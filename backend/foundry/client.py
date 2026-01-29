"""Azure AI Foundry Agent Client

This module provides a client for interacting with Azure AI Foundry agents
using the OpenAI-compatible API endpoint.
"""

import logging
import httpx
from typing import AsyncGenerator, Optional, Dict, Any
import json

logger = logging.getLogger(__name__)


class FoundryClient:
    """Client for Azure AI Foundry Agent API"""
    
    def __init__(
        self,
        endpoint: str,
        bearer_token: Optional[str] = None,
        credential = None,
        timeout: float = 30.0
    ):
        """
        Initialize Foundry client.
        
        Args:
            endpoint: The OpenAI-compatible responses endpoint URL
            bearer_token: Bearer token for authentication (optional if credential is provided)
            credential: Azure credential object (e.g., DefaultAzureCredential)
            timeout: Request timeout in seconds
        """
        self.endpoint = endpoint
        self.bearer_token = bearer_token
        self.credential = credential
        self.timeout = timeout
        self._client = httpx.AsyncClient(timeout=timeout)
        self._cached_token = None
    
    async def close(self):
        """Close the HTTP client"""
        await self._client.aclose()
    
    async def _get_bearer_token(self) -> str:
        """Get bearer token either from static token or Azure credential"""
        if self.bearer_token:
            logger.debug(f"Using provided bearer token: {self.bearer_token[:10]}...")
            return self.bearer_token
        
        if self.credential:
            try:
                # Get token for Azure AI services using async method
                # Use ai.azure.com scope for Azure AI Foundry
                logger.debug("Requesting token from Azure Identity...")
                token = await self.credential.get_token("https://ai.azure.com/.default")
                logger.debug(f"Token acquired: {token.token[:20]}...")
                return token.token
            except Exception as e:
                logger.error(f"Failed to get token from Azure Identity: {str(e)}")
                raise
        
        raise ValueError("Either bearer_token or credential must be provided")
    
    async def send_message(
        self,
        messages: list,
        stream: bool = True,
        **kwargs
    ) -> AsyncGenerator[str, None]:
        """
        Send a message to the Foundry agent and stream the response.
        
        Args:
            messages: List of message dictionaries (OpenAI format)
            stream: Whether to stream the response
            **kwargs: Additional parameters to pass to the API
            
        Yields:
            Response chunks as they arrive
        """
        try:
            token = await self._get_bearer_token()
            
            if not token or len(token.strip()) == 0:
                raise ValueError("Bearer token is empty or invalid")
            
            logger.debug(f"Using bearer token: {token[:30]}...")
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            }
        except Exception as e:
            logger.error(f"Failed to get bearer token: {str(e)}")
            raise
        
        
        
        
        
        
        
        # Foundry Responses API format
        # Last message goes to 'input', previous messages go to 'conversationHistory'
        if not messages:
            raise ValueError("Messages cannot be empty")
        
        # Extract the last user message for 'input'
        last_message = messages[-1]
        input_text = last_message.get("content", "")
        
        # Previous messages become conversation history
        conversation_history = []
        if len(messages) > 1:
            for msg in messages[:-1]:
                conversation_history.append({
                    "role": msg.get("role", "user"),
                    "content": msg.get("content", "")
                })
        
        payload = {
            "input": input_text,
            "stream": stream,
            **kwargs
        }
        
        # Only add conversationHistory if there are previous messages
        if conversation_history:
            payload["conversationHistory"] = conversation_history
        
        logger.debug(f"Sending request to Foundry: {self.endpoint}")
        logger.debug(f"Input with {len(conversation_history)} history messages")
        
        try:
            if stream:
                async with self._client.stream(
                    "POST",
                    self.endpoint,
                    json=payload,
                    headers=headers
                ) as response:
                    response.raise_for_status()
                    
                    async for line in response.aiter_lines():
                        if line.strip():
                            # Handle Server-Sent Events format
                            if line.startswith("data: "):
                                data = line[6:]  # Remove "data: " prefix
                                if data.strip() == "[DONE]":
                                    break
                                yield data
                            else:
                                yield line
            else:
                response = await self._client.post(
                    self.endpoint,
                    json=payload,
                    headers=headers
                )
                response.raise_for_status()
                yield response.text
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            raise
        except httpx.RequestError as e:
            logger.error(f"Request error occurred: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise
    
    async def send_message_non_streaming(
        self,
        messages: list,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Send a message to the Foundry agent and get the complete response.
        
        Args:
            messages: List of message dictionaries (OpenAI format)
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            Complete response as a dictionary
        """
        try:
            token = await self._get_bearer_token()
            
            if not token or len(token.strip()) == 0:
                raise ValueError("Bearer token is empty or invalid")
            
            logger.debug(f"Using bearer token: {token[:30]}...")
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            }
        except Exception as e:
            logger.error(f"Failed to get bearer token: {str(e)}")
            raise
        
        # Foundry Responses API format
        # Last message goes to 'input', previous messages go to 'conversationHistory'
        if not messages:
            raise ValueError("Messages cannot be empty")
        
        # Extract the last user message for 'input'
        last_message = messages[-1]
        input_text = last_message.get("content", "")
        
        # Previous messages become conversation history
        conversation_history = []
        if len(messages) > 1:
            for msg in messages[:-1]:
                conversation_history.append({
                    "role": msg.get("role", "user"),
                    "content": msg.get("content", "")
                })
        
        payload = {
            "input": input_text,
            "stream": False,
            **kwargs
        }
        
        # Only add conversationHistory if there are previous messages
        if conversation_history:
            payload["conversationHistory"] = conversation_history
        
        logger.debug(f"Sending request with input and {len(conversation_history)} history messages")
        logger.debug(f"Payload: {json.dumps(payload, indent=2)}")
        
        logger.debug(f"Sending non-streaming request to Foundry: {self.endpoint}")
        
        try:
            response = await self._client.post(
                self.endpoint,
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error occurred: {e.response.status_code}")
            logger.error(f"Response text: {e.response.text}")
            logger.error(f"Request payload: {json.dumps(payload, indent=2)}")
            raise
        except httpx.RequestError as e:
            logger.error(f"Request error occurred: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise
