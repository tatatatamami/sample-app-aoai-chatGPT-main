# -*- coding: utf-8 -*-
"""Test Foundry with Azure Identity"""
import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from backend.settings import app_settings
from backend.foundry.client import FoundryClient

async def test_settings():
    print("=" * 60)
    print("Testing Foundry Settings")
    print("=" * 60)
    if not app_settings.foundry:
        print("X Foundry settings not loaded")
        return False
    print(f"OK Foundry Enabled: {app_settings.foundry.enabled}")
    print(f"OK Use Azure Identity: {app_settings.foundry.use_azure_identity}")
    print(f"OK Endpoint: {app_settings.foundry.get_responses_endpoint()}")
    return True

async def test_client():
    print("\\n" + "=" * 60)
    print("Testing Foundry Client with Azure Identity")
    print("=" * 60)
    if not app_settings.foundry or not app_settings.foundry.use_azure_identity:
        print("X Azure Identity not enabled")
        return False
    try:
        from azure.identity import DefaultAzureCredential
        credential = DefaultAzureCredential()
        client = FoundryClient(
            endpoint=app_settings.foundry.get_responses_endpoint(),
            credential=credential,
            timeout=30.0
        )
        print("OK Client initialized")
        await client.close()
        return True
    except Exception as e:
        print(f"X Failed: {str(e)}")
        return False

async def main():
    print("\\nFoundry Test with Azure Identity\\n")
    s = await test_settings()
    c = await test_client()
    print("\\n" + "=" * 60)
    print(f"Settings: {'PASS' if s else 'FAIL'}")
    print(f"Client: {'PASS' if c else 'FAIL'}")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
