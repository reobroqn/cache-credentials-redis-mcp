#!/usr/bin/env python3
"""
Simple test script to test FastMCP client authentication with stdio transport
"""

import asyncio
import sys
import os
from pathlib import Path

# Add src to path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fastmcp import Client
from fastmcp.client.logging import LogMessage


async def log_handler(message: LogMessage):
    """Handle server log messages"""
    print(f"[SERVER LOG] {message.data}")


async def progress_handler(progress: float, total: float | None, message: str | None):
    """Handle progress messages"""
    print(f"[PROGRESS] {progress}/{total} - {message or ''}")


async def test_client_connection():
    """Test basic client connection and tool calls"""
    
    # Path to our server script
    server_path = Path(__file__).parent.parent / "src" / "server.py"
    
    print(f"Testing client connection to server: {server_path}")
    print("=" * 60)
    
    # Create client with our server
    client = Client(
        str(server_path),
        log_handler=log_handler,
        progress_handler=progress_handler,
        timeout=30.0
    )
    
    try:
        async with client:
            print("✅ Client connected successfully")
            
            # Test basic server ping
            print("\n📞 Testing server ping...")
            ping_result = await client.ping()
            print(f"   Ping result: {ping_result}")
            
            # List available tools
            print("\n🔧 Listing available tools...")
            tools = await client.list_tools()
            print(f"   Found {len(tools)} tools:")
            for tool in tools:
                print(f"   - {tool.name}: {tool.description}")
            
            # Test api_get_user_data tool
            print("\n👤 Testing api_get_user_data tool...")
            try:
                result = await client.call_tool("api_get_user_data", {"user_id": "test_123"})
                print(f"   ✅ Tool call successful")
                print(f"   Result: {result}")
            except Exception as e:
                print(f"   ❌ Tool call failed: {e}")
                print(f"   Error type: {type(e).__name__}")
            
            # Test db_query_users tool  
            print("\n🗄️  Testing db_query_users tool...")
            try:
                result = await client.call_tool("db_query_users", {"limit": 5})
                print(f"   ✅ Tool call successful")
                print(f"   Result: {result}")
            except Exception as e:
                print(f"   ❌ Tool call failed: {e}")
                print(f"   Error type: {type(e).__name__}")
            
            print("\n🏁 Test completed")
            
    except Exception as e:
        print(f"❌ Client connection failed: {e}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()


async def test_authentication_flow():
    """Test what happens with authentication in our current setup"""
    
    print("\n" + "=" * 60)
    print("🔐 AUTHENTICATION FLOW TEST")
    print("=" * 60)
    
    # Test with no explicit authentication
    print("Testing with current setup (no explicit auth)...")
    print("This will show us what get_access_token() returns")
    
    server_path = Path(__file__).parent.parent / "src" / "server.py"
    
    client = Client(
        str(server_path),
        log_handler=log_handler,
        timeout=30.0
    )
    
    try:
        async with client:
            # This should trigger our middleware and show what happens
            result = await client.call_tool("api_get_user_data", {"user_id": "auth_test"})
            print(f"Result with current auth: {result}")
            
    except Exception as e:
        print(f"Auth test error: {e}")
        print(f"Error type: {type(e).__name__}")
        
        # This will help us understand the authentication flow
        if "No access token found" in str(e):
            print("🔍 Our middleware correctly detected no access token")
        elif "credentials" in str(e).lower():
            print("🔍 Issue is related to credentials")
        else:
            print("🔍 Different error - need to investigate")


async def main():
    """Main test function"""
    print("🚀 Starting FastMCP Client Authentication Test")
    print(f"Working directory: {os.getcwd()}")
    print(f"Python path: {sys.path[:3]}...")  # Show first few entries
    
    # Test basic connection first
    await test_client_connection()
    
    # Test authentication flow
    await test_authentication_flow()
    
    print("\n🎯 Test script completed - check the output above")


if __name__ == "__main__":
    asyncio.run(main())
