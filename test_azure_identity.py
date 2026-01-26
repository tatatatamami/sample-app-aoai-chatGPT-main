# -*- coding: utf-8 -*-
"""Test Azure Identity with Foundry Agent"""

import asyncio
from azure.identity import DefaultAzureCredential

async def test_azure_identity():
    print("Testing Azure Identity for Foundry Agent")
    print("=" * 60)
    
    try:
        # Create credential
        credential = DefaultAzureCredential()
        
        # Get token for Azure AI services
        token = credential.get_token("https://ai.azure.com/.default")
        
        print(f"? Token acquired successfully")
        print(f"   Token (last 10 chars): ...{token.token[-10:]}")
        print(f"   Expires on: {token.expires_on}")
        
        return True
        
    except Exception as e:
        print(f"? Failed to get token: {str(e)}")
        print("\n?? Make sure you are logged in to Azure:")
        print("   Run: az login")
        return False


if __name__ == "__main__":
    asyncio.run(test_azure_identity())
