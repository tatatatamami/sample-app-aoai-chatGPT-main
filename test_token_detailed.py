# -*- coding: utf-8 -*-
"""Test token acquisition with detailed logging"""

import asyncio
from azure.identity.aio import DefaultAzureCredential

async def test_token_acquisition():
    print("Testing Token Acquisition")
    print("=" * 60)
    
    try:
        credential = DefaultAzureCredential()
        print("? DefaultAzureCredential created")
        
        scope = "https://cognitiveservices.azure.com/.default"
        print(f"\n?? Requesting token for scope: {scope}")
        
        token = await credential.get_token(scope)
        
        print(f"\n? Token acquired successfully!")
        print(f"   Token type: {type(token)}")
        print(f"   Token length: {len(token.token)}")
        print(f"   Token preview: {token.token[:50]}...")
        print(f"   Token end: ...{token.token[-20:]}")
        print(f"   Expires on: {token.expires_on}")
        
        # Check if token is valid
        if not token.token or len(token.token.strip()) == 0:
            print("\n? ERROR: Token is empty!")
            return False
        
        print("\n? Token validation: OK")
        
        await credential.close()
        return True
        
    except Exception as e:
        print(f"\n? Failed to get token: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_token_acquisition())
    if success:
        print("\n?? Token acquisition test PASSED")
    else:
        print("\n? Token acquisition test FAILED")
