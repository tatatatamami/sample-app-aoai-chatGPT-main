using FoundryChat.Models;

namespace FoundryChat.Services;

/// <summary>
/// Interface for Azure AI Foundry client
/// </summary>
public interface IFoundryClient
{
    /// <summary>
    /// Sends a message to the Foundry agent and streams the response
    /// </summary>
    IAsyncEnumerable<string> SendMessageAsync(List<ChatMessage> messages, bool stream = true, CancellationToken cancellationToken = default);

    /// <summary>
    /// Sends a message to the Foundry agent and gets the complete response
    /// </summary>
    Task<string> SendMessageNonStreamingAsync(List<ChatMessage> messages, CancellationToken cancellationToken = default);
}
