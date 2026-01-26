# Palantir Foundry Agent Integration

This document describes how to integrate and use Palantir Foundry agents with the Azure OpenAI chat application.

## Overview

The application now supports two backend options:
- **Azure OpenAI** (default) - Uses Azure OpenAI's GPT models
- **Palantir Foundry Agent** - Uses custom agents built in Palantir Foundry

Users can switch between these backends by configuring environment variables.

## Configuration

### Environment Variables

Add the following environment variables to your `.env` file:

```bash
# Enable/Disable Foundry Agent
FOUNDRY_ENABLED=True

# Foundry API Endpoint
FOUNDRY_ENDPOINT=https://your-foundry-instance.palantirfoundry.com/api/agent

# Foundry Bearer Token for Authentication
FOUNDRY_BEARER_TOKEN=your-bearer-token-here
```

### Configuration Options

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `FOUNDRY_ENABLED` | No | `False` | Enable or disable Foundry agent integration |
| `FOUNDRY_ENDPOINT` | Yes* | - | The Foundry API endpoint URL |
| `FOUNDRY_BEARER_TOKEN` | Yes* | - | Bearer token for authenticating with Foundry API |

\* Required only when `FOUNDRY_ENABLED=True`

## How It Works

### Request Routing

When `FOUNDRY_ENABLED=True`, all conversation requests are routed to the Foundry agent instead of Azure OpenAI. The routing logic is implemented in the `conversation_internal()` function in `app.py`.

### Request Format

The application sends requests to Foundry with the following JSON structure:

```json
{
  "message": "Current user message",
  "history": [
    {"role": "user", "content": "Previous user message"},
    {"role": "assistant", "content": "Previous assistant response"}
  ]
}
```

### Response Format

The Foundry agent should return a JSON response with the following structure:

```json
{
  "response": "Agent's response message"
}
```

Or alternatively:

```json
{
  "message": "Agent's response message"
}
```

## Authentication

The application uses Bearer Token authentication when communicating with Foundry. The token is sent in the `Authorization` header:

```
Authorization: Bearer <your-bearer-token>
```

## Backend Selection

### Using Foundry Agent

To use the Foundry agent, set:
```bash
FOUNDRY_ENABLED=True
FOUNDRY_ENDPOINT=https://your-foundry-instance.example.com/api/agent
FOUNDRY_BEARER_TOKEN=your-token
```

### Using Azure OpenAI (Default)

To use Azure OpenAI, either:
- Set `FOUNDRY_ENABLED=False`, or
- Don't set the `FOUNDRY_ENABLED` variable at all

The Azure OpenAI configuration remains unchanged and continues to work as before.

## Features

### Supported Features
- ✅ Basic chat conversation
- ✅ Conversation history context
- ✅ Bearer Token authentication
- ✅ Backend selection via environment variable
- ✅ Frontend settings include Foundry status

### Not Yet Supported
- ⚠️ Streaming responses (Foundry responses are non-streaming)
- ⚠️ Function calling (not implemented for Foundry)

## Example Usage

1. **Set up your `.env` file:**
   ```bash
   # Azure OpenAI settings (required)
   AZURE_OPENAI_MODEL=gpt-35-turbo
   AZURE_OPENAI_ENDPOINT=https://your-instance.openai.azure.com
   
   # Foundry settings
   FOUNDRY_ENABLED=True
   FOUNDRY_ENDPOINT=https://demo.palantirfoundry.com/api/agent
   FOUNDRY_BEARER_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```

2. **Start the application:**
   ```bash
   python -m gunicorn app:create_app
   ```

3. **Send a chat request:**
   The application will automatically route to Foundry when enabled.

## Testing

### Unit Tests

The integration includes comprehensive unit tests:

```bash
# Run all tests
pytest tests/unit_tests/

# Run Foundry-specific tests
pytest tests/unit_tests/test_foundry.py

# Run settings tests
pytest tests/unit_tests/test_settings.py::test_dotenv_foundry_enabled
pytest tests/unit_tests/test_settings.py::test_dotenv_foundry_disabled
```

### Manual Testing

To test the Foundry integration manually:

1. Configure your `.env` with valid Foundry credentials
2. Start the application
3. Send a chat message through the UI or API
4. Verify that the response comes from Foundry

## Troubleshooting

### Common Issues

**Issue: "Foundry is not configured or not enabled"**
- Check that `FOUNDRY_ENABLED=True` in your `.env` file
- Verify that `FOUNDRY_ENDPOINT` and `FOUNDRY_BEARER_TOKEN` are set

**Issue: "HTTP error in Foundry request"**
- Verify your Bearer token is valid and not expired
- Check that the Foundry endpoint URL is correct
- Ensure your network can reach the Foundry endpoint

**Issue: Foundry returns unexpected response format**
- Check the application logs for the actual response structure
- The application expects either `response` or `message` field in the JSON

## Security Considerations

- Store the `FOUNDRY_BEARER_TOKEN` securely and never commit it to version control
- Use environment variables or a secure secret management system
- Rotate tokens regularly according to your organization's security policy
- Ensure HTTPS is used for all Foundry API communications

## Additional Resources

- [Azure OpenAI Documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
- [Palantir Foundry Documentation](https://www.palantir.com/docs/foundry/)
