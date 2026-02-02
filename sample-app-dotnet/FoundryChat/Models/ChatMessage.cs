namespace FoundryChat.Models;

/// <summary>
/// Represents a chat message in OpenAI format
/// </summary>
public class ChatMessage
{
    public string Role { get; set; } = string.Empty;
    public string Content { get; set; } = string.Empty;
}
