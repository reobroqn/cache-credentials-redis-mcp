#!/usr/bin/env python3
"""
Simple test script to test FastMCP client authentication with HTTP transport and JWT
"""

import asyncio
import sys
import time
import jwt
from pathlib import Path

# Add src to path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from settings import settings

from fastmcp import Client
from fastmcp.client.logging import LogMessage
from fastmcp.client.transports import StreamableHttpTransport
from fastmcp.client.auth import BearerAuth

# Global server URL
SERVER_URL = "http://localhost:8000/mcp"


def generate_jwt_token(customer_id: str = "test_customer_123") -> str:
    """Generate a JWT token for testing FastMCP authentication"""

    payload = {
        "customer_id": customer_id,  # This matches what our middleware expects
        "iss": "fastmcp-test",  # Issuer - must match server config
        "aud": "fastmcp-credential-demo",  # Audience - must match server config
        "iat": int(time.time()),  # Issued at
        "exp": int(time.time()) + 3600,  # Expires in 1 hour
        "sub": customer_id,  # Subject (fallback)
    }

    token = jwt.encode(payload, settings.JWT_SIGNING_KEY, algorithm="HS256")

    return token


async def log_handler(message: LogMessage):
    """Handle server log messages"""
    print(f"[LOG] {message.data}")


async def test_with_jwt_auth():
    """Test client connection with JWT authentication"""

    print("\nTesting connection WITH JWT authentication...")

    # Generate JWT token
    token = generate_jwt_token("test_customer_123")
    print(f"🔑 Generated JWT token: {token[:30]}...")

    # Create client with JWT authentication
    transport = StreamableHttpTransport(url=SERVER_URL)
    client = Client(
        transport, auth=BearerAuth(token=token), log_handler=log_handler, timeout=30.0
    )

    try:
        async with client:
            print("✅ Client connected with JWT!")

            # Test server ping
            ping_result = await client.ping()
            print(f"Ping: {ping_result}")

            # List tools
            tools = await client.list_tools()
            print(f"Tools found: {len(tools)}")
            for tool in tools:
                print(f"  - {tool.name}")

            # Test api_get_user_data
            result = await client.call_tool(
                "api_get_user_data", {"user_id": "test_123"}
            )
            print(f"api_get_user_data result: {result}")

            # Test db_query_users
            result = await client.call_tool("db_query_users", {"limit": 5})
            print(f"db_query_users result: {result}")

    except Exception as e:
        print(f"❌ JWT auth failed: {e}")


async def main():
    """Main test function"""
    print("FastMCP Client JWT Authentication Test")
    print("=" * 50)

    # Test with JWT auth
    await test_with_jwt_auth()

    print("\n🏁 JWT authentication tests completed")


if __name__ == "__main__":
    asyncio.run(main())
