using System.Net.Http.Headers;
using System.Runtime.CompilerServices;
using System.Text;
using System.Text.Json;
using Azure.Core;
using Azure.Identity;
using FoundryChat.Models;

namespace FoundryChat.Services;

/// <summary>
/// Client for Azure AI Foundry Agent API
/// </summary>
public class FoundryClient : IFoundryClient
{
    private readonly HttpClient _httpClient;
    private readonly FoundrySettings _settings;
    private readonly TokenCredential? _credential;
    private readonly ILogger<FoundryClient> _logger;

    public FoundryClient(
        HttpClient httpClient,
        FoundrySettings settings,
        ILogger<FoundryClient> logger)
    {
        _httpClient = httpClient ?? throw new ArgumentNullException(nameof(httpClient));
        _settings = settings ?? throw new ArgumentNullException(nameof(settings));
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));

        // Configure timeout
        _httpClient.Timeout = TimeSpan.FromSeconds(_settings.ResponseTimeout);

        // Initialize credential if using Azure Identity
        if (_settings.UseAzureIdentity)
        {
            _credential = new DefaultAzureCredential();
            _logger.LogInformation("Using Azure Identity (DefaultAzureCredential) for Foundry authentication");
        }
        else if (string.IsNullOrWhiteSpace(_settings.BearerToken))
        {
            _logger.LogWarning("Foundry is enabled but neither BearerToken nor UseAzureIdentity is configured");
        }
    }

    /// <summary>
    /// Gets bearer token either from static token or Azure credential
    /// </summary>
    private async Task<string> GetBearerTokenAsync(CancellationToken cancellationToken = default)
    {
        if (!string.IsNullOrWhiteSpace(_settings.BearerToken))
        {
            _logger.LogDebug("Using provided bearer token");
            return _settings.BearerToken;
        }

        if (_credential != null)
        {
            try
            {
                _logger.LogDebug("Requesting token from Azure Identity...");
                // Use https://ai.azure.com/.default scope for Azure AI Foundry
                var tokenRequestContext = new TokenRequestContext(new[] { "https://ai.azure.com/.default" });
                var token = await _credential.GetTokenAsync(tokenRequestContext, cancellationToken);
                _logger.LogDebug($"Token acquired: {token.Token[..Math.Min(20, token.Token.Length)]}...");
                return token.Token;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to get token from Azure Identity");
                throw;
            }
        }

        throw new InvalidOperationException("Either BearerToken or Azure Identity credential must be provided");
    }

    /// <summary>
    /// Sends a message to the Foundry agent and streams the response
    /// </summary>
    public async IAsyncEnumerable<string> SendMessageAsync(
        List<ChatMessage> messages,
        bool stream = true,
        [EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        var token = await GetBearerTokenAsync(cancellationToken);

        if (string.IsNullOrWhiteSpace(token))
        {
            throw new InvalidOperationException("Bearer token is empty or invalid");
        }

        // Extract the last user message
        var userMessage = messages.LastOrDefault(m => m.Role == "user")?.Content;
        if (string.IsNullOrWhiteSpace(userMessage))
        {
            throw new ArgumentException("No user message found in messages");
        }

        var endpoint = _settings.GetResponsesEndpoint();
        var payload = new
        {
            input = userMessage,
            stream = stream
        };

        _logger.LogDebug($"Sending request to Foundry: {endpoint}");
        _logger.LogDebug($"Payload: {JsonSerializer.Serialize(payload)}");

        var request = new HttpRequestMessage(HttpMethod.Post, endpoint)
        {
            Content = new StringContent(JsonSerializer.Serialize(payload), Encoding.UTF8, "application/json")
        };
        request.Headers.Authorization = new AuthenticationHeaderValue("Bearer", token);

        HttpResponseMessage? response = null;
        
        try
        {
            response = await _httpClient.SendAsync(request, HttpCompletionOption.ResponseHeadersRead, cancellationToken);
            response.EnsureSuccessStatusCode();
        }
        catch (HttpRequestException ex)
        {
            _logger.LogError(ex, $"HTTP error occurred: {ex.Message}");
            throw;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, $"Unexpected error: {ex.Message}");
            throw;
        }

        // Yield results outside of try-catch
        if (stream)
        {
            using (response)
            {
                using var responseStream = await response.Content.ReadAsStreamAsync(cancellationToken);
                using var reader = new StreamReader(responseStream);

                while (!reader.EndOfStream && !cancellationToken.IsCancellationRequested)
                {
                    var line = await reader.ReadLineAsync(cancellationToken);
                    if (string.IsNullOrWhiteSpace(line))
                        continue;

                    // Handle Server-Sent Events format
                    if (line.StartsWith("data: "))
                    {
                        var data = line.Substring(6); // Remove "data: " prefix
                        if (data.Trim() == "[DONE]")
                            break;
                        
                        yield return data;
                    }
                    else
                    {
                        yield return line;
                    }
                }
            }
        }
        else
        {
            using (response)
            {
                var content = await response.Content.ReadAsStringAsync(cancellationToken);
                yield return content;
            }
        }
    }

    /// <summary>
    /// Sends a message to the Foundry agent and gets the complete response
    /// </summary>
    public async Task<string> SendMessageNonStreamingAsync(
        List<ChatMessage> messages,
        CancellationToken cancellationToken = default)
    {
        var token = await GetBearerTokenAsync(cancellationToken);

        if (string.IsNullOrWhiteSpace(token))
        {
            throw new InvalidOperationException("Bearer token is empty or invalid");
        }

        // Extract the last user message
        var userMessage = messages.LastOrDefault(m => m.Role == "user")?.Content;
        if (string.IsNullOrWhiteSpace(userMessage))
        {
            throw new ArgumentException("No user message found in messages");
        }

        var endpoint = _settings.GetResponsesEndpoint();
        var payload = new
        {
            input = userMessage,
            stream = false
        };

        _logger.LogDebug($"Sending non-streaming request to Foundry: {endpoint}");

        var request = new HttpRequestMessage(HttpMethod.Post, endpoint)
        {
            Content = new StringContent(JsonSerializer.Serialize(payload), Encoding.UTF8, "application/json")
        };
        request.Headers.Authorization = new AuthenticationHeaderValue("Bearer", token);

        try
        {
            using var response = await _httpClient.SendAsync(request, cancellationToken);
            response.EnsureSuccessStatusCode();

            var content = await response.Content.ReadAsStringAsync(cancellationToken);
            return content;
        }
        catch (HttpRequestException ex)
        {
            _logger.LogError(ex, $"HTTP error occurred: {ex.Message}");
            throw;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, $"Unexpected error: {ex.Message}");
            throw;
        }
    }
}
