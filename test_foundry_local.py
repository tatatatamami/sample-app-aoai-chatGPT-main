# -*- coding: utf-8 -*-
"""Test Foundry Client locally"""
import asyncio
import os
from azure.identity.aio import DefaultAzureCredential
from backend.foundry.client import FoundryClient
from backend.settings import app_settings

async def test_foundry():
    """Test Foundry client with a simple message"""
    
    # Get settings
    foundry = app_settings.foundry
    
    print(f"Endpoint: {foundry.endpoint}")
    print(f"Project: {foundry.project}")
    print(f"Application: {foundry.application}")
    print(f"Use Azure Identity: {foundry.use_azure_identity}")
    
    # Build full endpoint URL
    endpoint = f"{foundry.endpoint}/api/projects/{foundry.project}/applications/{foundry.application}/protocols/openai/responses?api-version={foundry.api_version}"
    print(f"\nFull endpoint: {endpoint}\n")
    
    # Create credential if needed
    credential = None
    if foundry.use_azure_identity:
        credential = DefaultAzureCredential()
        print("Using Azure DefaultAzureCredential\n")
    
    # Create client
    client = FoundryClient(
        endpoint=endpoint,
        bearer_token=foundry.bearer_token,
        credential=credential,
        timeout=60.0
    )
    
    # Test messages
    messages = [
        {
            "role": "user",
            "content": "Tell me about incident response"  # Changed to English
        }
    ]
    
    print("Sending test message...\n")
    
    try:
        # Test non-streaming
        response = await client.send_message_non_streaming(messages)
        print("? Success!")
        print(f"\nResponse: {response}\n")
        
    except Exception as e:
        print(f"? Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        await client.close()
        if credential:
            await credential.close()

if __name__ == "__main__":
    asyncio.run(test_foundry())
