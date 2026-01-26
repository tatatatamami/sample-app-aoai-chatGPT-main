# -*- coding: utf-8 -*-
"""Test Azure Identity scopes for Foundry"""

import asyncio
from azure.identity.aio import DefaultAzureCredential

async def test_scopes():
    print("Testing different Azure scopes for Foundry Agent")
    print("=" * 60)
    
    credential = DefaultAzureCredential()
    
    # Try different scopes
    scopes = [
        "https://cognitiveservices.azure.com/.default",
        "https://ai.azure.com/.default",
        "https://management.azure.com/.default",
    ]
    
    for scope in scopes:
        print(f"\nTrying scope: {scope}")
        try:
            token = await credential.get_token(scope)
            print(f"  ? Success! Token: ...{token.token[-10:]}")
        except Exception as e:
            print(f"  ? Failed: {str(e)}")
    
    await credential.close()

if __name__ == "__main__":
    asyncio.run(test_scopes())
