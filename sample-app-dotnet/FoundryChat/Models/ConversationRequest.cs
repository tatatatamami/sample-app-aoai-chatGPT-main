namespace FoundryChat.Models;

/// <summary>
/// Request model for conversation endpoint
/// </summary>
public class ConversationRequest
{
    public List<ChatMessage> Messages { get; set; } = new();
    public bool Stream { get; set; } = true;
}
