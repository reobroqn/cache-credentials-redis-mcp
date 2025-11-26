#!/usr/bin/env python3
"""
Simple test script to test FastMCP client authentication with HTTP transport
"""

import asyncio
import sys
from pathlib import Path

# Add src to path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fastmcp import Client
from fastmcp.client.logging import LogMessage
from fastmcp.client.transports import StreamableHttpTransport

# Global server URL
SERVER_URL = "http://localhost:8000/mcp"


async def log_handler(message: LogMessage):
    """Handle server log messages"""
    print(f"[LOG] {message.data}")


async def test_client_connection():
    """Test basic client connection and tool calls"""

    print(f"Testing client connection to: {SERVER_URL}")

    # Create HTTP transport
    transport = StreamableHttpTransport(url=SERVER_URL)
    client = Client(transport, log_handler=log_handler, timeout=30.0)

    async with client:
        print("✅ Client connected")

        # Test server ping
        ping_result = await client.ping()
        print(f"Ping: {ping_result}")

        # List tools
        tools = await client.list_tools()
        print(f"Tools found: {len(tools)}")
        for tool in tools:
            print(f"  - {tool.name}")

        # Test api_get_user_data
        result = await client.call_tool("api_get_user_data", {"user_id": "test_123"})
        print(f"api_get_user_data result: {result}")

        # Test db_query_users
        result = await client.call_tool("db_query_users", {"limit": 5})
        print(f"db_query_users result: {result}")


async def test_authentication_flow():
    """Test authentication flow"""

    print("\nTesting authentication flow...")

    transport = StreamableHttpTransport(url=SERVER_URL)
    client = Client(transport, log_handler=log_handler, timeout=30.0)

    async with client:
        result = await client.call_tool("api_get_user_data", {"user_id": "auth_test"})
        print(f"Auth test result: {result}")


async def test_health_endpoint():
    """Test health endpoint directly"""

    print("\nTesting health endpoint...")

    import aiohttp

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:8000/health") as response:
                if response.status == 200:
                    health_data = await response.json()
                    print(f"Health check: {health_data}")
                else:
                    print(f"Health check failed: {response.status}")
    except Exception as e:
        print(f"Health check error: {e}")


async def main():
    """Main test function"""
    print("FastMCP Client HTTP Transport Test")

    # Test health endpoint first
    await test_health_endpoint()

    # Test client connection
    await test_client_connection()

    # Test authentication flow
    await test_authentication_flow()

    print("Test completed")


if __name__ == "__main__":
    asyncio.run(main())
