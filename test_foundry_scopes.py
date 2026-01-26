# -*- coding: utf-8 -*-
"""Test different Azure scopes for Foundry Agent authentication"""

import asyncio
import httpx
from azure.identity.aio import DefaultAzureCredential

FOUNDRY_ENDPOINT = "https://demo-kddi-resource.services.ai.azure.com/api/projects/demo-kddi/applications/IncidentKnowledgeAgent/protocols/openai/responses?api-version=2025-11-15-preview"

async def test_scope(scope):
    """Test API call with a specific scope"""
    print(f"\n{'='*60}")
    print(f"Testing scope: {scope}")
    print(f"{'='*60}")
    
    try:
        credential = DefaultAzureCredential()
        token = await credential.get_token(scope)
        
        print(f"? Token acquired: {token.token[:30]}...")
        
        # Test API call
        headers = {
            "Authorization": f"Bearer {token.token}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "messages": [
                {"role": "user", "content": "Hello"}
            ]
        }
        
        print(f"?? Testing API call to Foundry...")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                FOUNDRY_ENDPOINT,
                json=payload,
                headers=headers
            )
            
            print(f"?? Status code: {response.status_code}")
            
            if response.status_code == 200:
                print(f"? SUCCESS! This scope works!")
                print(f"Response: {response.text[:200]}...")
                return scope, True
            else:
                print(f"? Failed with status {response.status_code}")
                print(f"Response: {response.text[:200]}...")
                return scope, False
                
    except httpx.HTTPStatusError as e:
        print(f"? HTTP Error: {e.response.status_code} - {e.response.text[:200]}")
        return scope, False
    except Exception as e:
        print(f"? Error: {str(e)}")
        return scope, False
    finally:
        await credential.close()


async def main():
    print("\n?? Testing different Azure scopes for Foundry Agent\n")
    
    # Test multiple scopes
    scopes_to_test = [
        "https://cognitiveservices.azure.com/.default",
        "https://ml.azure.com/.default",
        "https://management.azure.com/.default",
        "https://ai.azure.com/.default",
        # Foundry-specific resource ID
        "https://demo-kddi-resource.services.ai.azure.com/.default",
    ]
    
    results = []
    for scope in scopes_to_test:
        scope_name, success = await test_scope(scope)
        results.append((scope_name, success))
        await asyncio.sleep(1)  # Small delay between tests
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    
    working_scopes = [s for s, success in results if success]
    
    if working_scopes:
        print(f"\n? Working scope(s):")
        for scope in working_scopes:
            print(f"   - {scope}")
    else:
        print(f"\n? No working scopes found.")
        print(f"\nPossible reasons:")
        print(f"1. User does not have permission to access the Foundry Agent")
        print(f"2. The API endpoint requires a different authentication method")
        print(f"3. The Foundry Agent is not properly configured")

if __name__ == "__main__":
    asyncio.run(main())
