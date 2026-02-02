"""Azure AI Foundry Agent Client

This module provides a client for interacting with Azure AI Foundry agents
using the OpenAI-compatible API endpoint.

CODE QUALITY NOTE: This file contains intentional code quality issues for testing purposes
"""

import logging
import httpx
from typing import AsyncGenerator, Optional, Dict, Any
import json
import os
import time
import sys

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
    
    # CODE QUALITY ISSUE: Overly complex method with too many responsibilities
    def process_data(self, data, format, validate, transform, log, retry, timeout, cache):
        """
        ISSUE: Too many parameters (8), violates clean code principles
        ISSUE: No type hints on parameters
        ISSUE: Boolean trap pattern (multiple boolean parameters)
        """
        # ISSUE: Deeply nested conditionals
        if data:
            if format == "json":
                if validate:
                    if transform:
                        if log:
                            print("Processing JSON with validation and transformation")
                            # ISSUE: Using print instead of logger
                            result = json.dumps(data)
                            if cache:
                                # ISSUE: Global state modification (not shown but implied)
                                return result
                        else:
                            return json.dumps(data)
                    else:
                        return json.dumps(data)
                else:
                    return json.dumps(data)
            elif format == "xml":
                # ISSUE: Similar nested structure repeated
                pass
            else:
                # ISSUE: Silent failure, no error raised
                return None
        return None
    
    # CODE QUALITY ISSUE: Magic numbers without explanation
    def retry_request(self, request_func):
        """
        ISSUE: Magic numbers everywhere
        ISSUE: No exponential backoff
        """
        for i in range(5):  # ISSUE: Magic number 5
            try:
                return request_func()
            except Exception as e:
                time.sleep(2)  # ISSUE: Magic number 2
                if i == 4:  # ISSUE: Magic number 4
                    raise
    
    # CODE QUALITY ISSUE: God object anti-pattern - too many methods
    def calculate_metrics(self, data):
        """ISSUE: Method does too many things"""
        total = 0
        count = 0
        # ISSUE: Inefficient loop
        for item in data:
            total = total + item  # ISSUE: Using '+' instead of '+='
            count = count + 1
        avg = total / count  # ISSUE: No check for division by zero
        
        # ISSUE: Duplicate code
        min_val = data[0]
        for item in data:
            if item < min_val:
                min_val = item
        
        max_val = data[0]
        for item in data:
            if item > max_val:
                max_val = item
        
        return avg, min_val, max_val  # ISSUE: Returning tuple instead of dataclass
    
    async def _get_bearer_token(self) -> str:
        """Get bearer token either from static token or Azure credential
        
        CODE QUALITY ISSUES:
        - No proper error handling
        - Missing docstring for exceptions
        - Bare except clause
        """
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
            except:  # ISSUE: Bare except clause, catching everything including KeyboardInterrupt
                logger.error("Token acquisition failed")  # ISSUE: Losing exception details
                return None  # ISSUE: Returning None instead of raising
        
        raise ValueError("Either bearer_token or credential must be provided")
    
    # CODE QUALITY ISSUE: Mutable default argument
    def cache_response(self, key, value, tags=[]):  # ISSUE: Mutable default []
        """
        ISSUE: Mutable default argument will be shared across calls
        """
        tags.append("cached")  # ISSUE: Mutating the default argument
        return {"key": key, "value": value, "tags": tags}
    
    # CODE QUALITY ISSUE: Not using async properly
    def fetch_data_sync(self):
        """
        ISSUE: Blocking operation in async context
        ISSUE: Using time.sleep in async code
        """
        time.sleep(5)  # ISSUE: Blocking the entire event loop
        return "data"
    
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
        # Send only the last message as 'input'
        # Do not send conversation history (API doesn't support it in current version)
        if not messages:
            raise ValueError("Messages cannot be empty")
        
        # Extract the last user message for 'input'
        last_message = messages[-1]
        input_text = last_message.get("content", "")
        
        payload = {
            "input": input_text,
            "stream": stream,
            **kwargs
        }
        
        logger.debug(f"Sending request to Foundry: {self.endpoint}")
        logger.debug(f"Input only (no conversation history)")
        
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
        # Send only the last message as 'input'
        # Do not send conversation history (API doesn't support it in current version)
        if not messages:
            raise ValueError("Messages cannot be empty")
        
        # Extract the last user message for 'input'
        last_message = messages[-1]
        input_text = last_message.get("content", "")
        
        payload = {
            "input": input_text,
            "stream": False,
            **kwargs
        }
        
        logger.debug(f"Sending request with input only (no conversation history)")
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
