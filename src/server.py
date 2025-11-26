"""
FastMCP Server with Simplified Credential Storage Middleware

Simple demonstration of credential management using ValkeyStore
with Fernet encryption. Only 2-3 tools for clean demo.
"""

from typing import Any, Dict

from fastmcp import FastMCP, Context
from fastmcp.server.middleware.caching import ResponseCachingMiddleware
from fastmcp.server.middleware.error_handling import ErrorHandlingMiddleware
from fastmcp.utilities.logging import get_logger
from key_value.aio.stores.valkey import ValkeyStore

from settings import settings
from middlewares import CredentialMiddleware
from services.api import APIService
from services.database import DatabaseService

logger = get_logger(__name__)

# Initialize FastMCP server
mcp = FastMCP(settings.SERVER_NAME)

# Set up Valkey store for caching
valkey_store = ValkeyStore(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
)

# Add middleware
mcp.add_middleware(ErrorHandlingMiddleware())
mcp.add_middleware(CredentialMiddleware(valkey_store))
mcp.add_middleware(ResponseCachingMiddleware(cache_storage=valkey_store))


@mcp.tool()
async def api_get_user_data(user_id: str, ctx: Context) -> Dict[str, Any]:
    """
    Fetch user data from external API using stored credentials

    Args:
        user_id: The ID of the user to fetch
        ctx: FastMCP context for accessing credentials

    Returns:
        User data including name, email, and status
    """
    # Credentials are automatically injected by the middleware into context state
    credentials = ctx.get_state("_credentials") or {}

    api_service = APIService(credentials)
    user_data = await api_service.get_user_data(user_id)

    logger.info(f"Successfully fetched user data for {user_id}")
    return user_data


@mcp.tool()
async def db_query_users(ctx: Context, limit: int = 10) -> Dict[str, Any]:
    """
    Query users from database using stored credentials

    Args:
        ctx: FastMCP context for accessing credentials
        limit: Maximum number of users to return

    Returns:
        List of users with their details
    """
    # Get credentials from context state
    credentials = ctx.get_state("_credentials")

    db_service = DatabaseService(credentials)
    users = await db_service.query_users(limit)

    logger.info(f"Successfully queried {len(users)} users")
    return {"users": users, "count": len(users)}


@mcp.custom_route("GET", "/health")
async def health_check():
    """Health check endpoint for Docker health checks"""
    return {"status": "healthy", "server": settings.SERVER_NAME}


def main():
    """Main entry point for the FastMCP server"""
    logger.info(f"Starting FastMCP server: {settings.SERVER_NAME}")
    logger.info(f"Valkey connection: {settings.REDIS_URL}")

    # Run with HTTP transport for Docker deployment
    mcp.run(transport="http", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
