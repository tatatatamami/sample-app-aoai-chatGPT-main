import pytest
import json
from unittest.mock import AsyncMock, patch, MagicMock
import sys
import os

# Add the parent directory to the path so we can import the app module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


@pytest.mark.asyncio
async def test_send_foundry_request_success():
    """Test that send_foundry_request properly formats and sends requests."""
    with patch('app.app_settings') as mock_settings, \
         patch('app.httpx.AsyncClient') as mock_client:
        
        # Setup mock settings
        mock_foundry = MagicMock()
        mock_foundry.enabled = True
        mock_foundry.endpoint = "https://test-foundry.example.com/api"
        mock_foundry.bearer_token = "test-token"
        mock_settings.foundry = mock_foundry
        
        # Setup mock HTTP client
        mock_response = MagicMock()
        mock_response.json.return_value = {"response": "Test response from Foundry"}
        mock_response.raise_for_status = MagicMock()
        
        mock_client_instance = AsyncMock()
        mock_client_instance.post = AsyncMock(return_value=mock_response)
        mock_client.return_value.__aenter__.return_value = mock_client_instance
        
        # Import after patching
        from app import send_foundry_request
        
        # Test request
        request_body = {
            "messages": [
                {"role": "user", "content": "Hello, Foundry!"}
            ]
        }
        
        result = await send_foundry_request(request_body)
        
        # Assertions
        assert result == {"response": "Test response from Foundry"}
        mock_client_instance.post.assert_called_once()
        call_args = mock_client_instance.post.call_args
        assert call_args.kwargs['headers']['Authorization'] == "Bearer test-token"
        assert call_args.kwargs['json']['message'] == "Hello, Foundry!"


@pytest.mark.asyncio
async def test_send_foundry_request_not_enabled():
    """Test that send_foundry_request raises error when Foundry is not enabled."""
    with patch('app.app_settings') as mock_settings:
        
        # Setup mock settings with Foundry disabled
        mock_foundry = MagicMock()
        mock_foundry.enabled = False
        mock_settings.foundry = mock_foundry
        
        # Import after patching
        from app import send_foundry_request
        
        # Test request should raise ValueError
        request_body = {
            "messages": [
                {"role": "user", "content": "Hello, Foundry!"}
            ]
        }
        
        with pytest.raises(ValueError, match="Foundry is not configured or not enabled"):
            await send_foundry_request(request_body)


@pytest.mark.asyncio
async def test_complete_foundry_request_formats_response():
    """Test that complete_foundry_request properly formats the Foundry response."""
    with patch('app.send_foundry_request') as mock_send, \
         patch('app.uuid.uuid4') as mock_uuid, \
         patch('app.time.time') as mock_time:
        
        # Setup mocks
        mock_send.return_value = {"response": "This is a test response"}
        mock_uuid.return_value = "test-uuid-12345"
        mock_time.return_value = 1234567890.0
        
        # Import after patching
        from app import complete_foundry_request
        
        # Test request
        request_body = {
            "messages": [
                {"role": "user", "content": "Test question"}
            ],
            "history_metadata": {"test": "metadata"}
        }
        
        result = await complete_foundry_request(request_body)
        
        # Assertions
        assert result["model"] == "foundry-agent"
        assert result["id"] == "test-uuid-12345"
        assert result["created"] == 1234567890
        assert result["choices"][0]["messages"][0]["role"] == "assistant"
        assert result["choices"][0]["messages"][0]["content"] == "This is a test response"
        assert result["history_metadata"] == {"test": "metadata"}


@pytest.mark.asyncio
async def test_send_foundry_request_with_conversation_history():
    """Test that send_foundry_request includes conversation history."""
    with patch('app.app_settings') as mock_settings, \
         patch('app.httpx.AsyncClient') as mock_client:
        
        # Setup mock settings
        mock_foundry = MagicMock()
        mock_foundry.enabled = True
        mock_foundry.endpoint = "https://test-foundry.example.com/api"
        mock_foundry.bearer_token = "test-token"
        mock_settings.foundry = mock_foundry
        
        # Setup mock HTTP client
        mock_response = MagicMock()
        mock_response.json.return_value = {"response": "Test response"}
        mock_response.raise_for_status = MagicMock()
        
        mock_client_instance = AsyncMock()
        mock_client_instance.post = AsyncMock(return_value=mock_response)
        mock_client.return_value.__aenter__.return_value = mock_client_instance
        
        # Import after patching
        from app import send_foundry_request
        
        # Test request with conversation history
        request_body = {
            "messages": [
                {"role": "user", "content": "First question"},
                {"role": "assistant", "content": "First answer"},
                {"role": "user", "content": "Second question"}
            ]
        }
        
        result = await send_foundry_request(request_body)
        
        # Assertions
        call_args = mock_client_instance.post.call_args
        payload = call_args.kwargs['json']
        assert payload['message'] == "Second question"
        assert len(payload['history']) == 2
        assert payload['history'][0]['role'] == "user"
        assert payload['history'][0]['content'] == "First question"
        assert payload['history'][1]['role'] == "assistant"
        assert payload['history'][1]['content'] == "First answer"
