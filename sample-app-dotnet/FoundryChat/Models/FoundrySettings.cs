namespace FoundryChat.Models;

/// <summary>
/// Configuration settings for Azure AI Foundry
/// </summary>
public class FoundrySettings
{
    public bool Enabled { get; set; }
    public string Project { get; set; } = string.Empty;
    public string Application { get; set; } = string.Empty;
    public string Endpoint { get; set; } = string.Empty;
    public string? BearerToken { get; set; }
    public bool UseAzureIdentity { get; set; }
    public string ApiVersion { get; set; } = "2025-11-15-preview";
    public int ResponseTimeout { get; set; } = 30;

    /// <summary>
    /// Gets the OpenAI-compatible responses API endpoint
    /// </summary>
    public string GetResponsesEndpoint()
    {
        return $"{Endpoint}/api/projects/{Project}/applications/{Application}/protocols/openai/responses?api-version={ApiVersion}";
    }

    /// <summary>
    /// Gets the activity protocol endpoint
    /// </summary>
    public string GetActivityEndpoint()
    {
        return $"{Endpoint}/api/projects/{Project}/applications/{Application}/protocols/activityprotocol?api-version={ApiVersion}";
    }
}
