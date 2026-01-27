using System.Text;
using FoundryChat.Models;
using FoundryChat.Services;
using Microsoft.AspNetCore.Mvc;

namespace FoundryChat.Controllers;

/// <summary>
/// Controller for handling conversation with Azure AI Foundry Agent
/// </summary>
[ApiController]
[Route("api/[controller]")]
public class ConversationController : ControllerBase
{
    private readonly IFoundryClient _foundryClient;
    private readonly ILogger<ConversationController> _logger;
    private readonly FoundrySettings _settings;

    public ConversationController(
        IFoundryClient foundryClient,
        IConfiguration configuration,
        ILogger<ConversationController> logger)
    {
        _foundryClient = foundryClient ?? throw new ArgumentNullException(nameof(foundryClient));
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));
        
        _settings = new FoundrySettings();
        configuration.GetSection("Foundry").Bind(_settings);
    }

    /// <summary>
    /// POST /api/conversation - Handle conversation with Foundry Agent
    /// </summary>
    [HttpPost]
    public async Task<IActionResult> Post([FromBody] ConversationRequest request, CancellationToken cancellationToken)
    {
        if (!_settings.Enabled)
        {
            _logger.LogWarning("Foundry is not enabled");
            return BadRequest(new { error = "Foundry is not enabled" });
        }

        if (request?.Messages == null || request.Messages.Count == 0)
        {
            _logger.LogWarning("No messages provided in request");
            return BadRequest(new { error = "messages is required" });
        }

        try
        {
            if (request.Stream)
            {
                // Return streaming response as Server-Sent Events
                Response.Headers.Append("Content-Type", "text/event-stream");
                Response.Headers.Append("Cache-Control", "no-cache");
                Response.Headers.Append("X-Accel-Buffering", "no");

                await foreach (var chunk in _foundryClient.SendMessageAsync(request.Messages, true, cancellationToken))
                {
                    if (cancellationToken.IsCancellationRequested)
                        break;

                    var eventData = $"data: {chunk}\n\n";
                    await Response.Body.WriteAsync(Encoding.UTF8.GetBytes(eventData), cancellationToken);
                    await Response.Body.FlushAsync(cancellationToken);
                }

                // Send done signal
                var doneData = "data: [DONE]\n\n";
                await Response.Body.WriteAsync(Encoding.UTF8.GetBytes(doneData), cancellationToken);
                await Response.Body.FlushAsync(cancellationToken);

                return new EmptyResult();
            }
            else
            {
                // Return non-streaming response
                var result = await _foundryClient.SendMessageNonStreamingAsync(request.Messages, cancellationToken);
                return Content(result, "application/json");
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error during conversation with Foundry");
            return StatusCode(500, new { error = ex.Message });
        }
    }
}
