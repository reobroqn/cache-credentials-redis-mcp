"""
FastMCP Server with Simplified Credential Storage Middleware

Simple demonstration of credential management using ValkeyStore
with Fernet encryption. Only 2-3 tools for clean demo.
"""

from typing import Any, Dict

from fastmcp import FastMCP, Context
from fastmcp.server.middleware.caching import ResponseCachingMiddleware
from fastmcp.server.middleware.error_handling import ErrorHandlingMiddleware
from fastmcp.server.auth.providers.jwt import JWTVerifier
from fastmcp.utilities.logging import get_logger
from key_value.aio.stores.valkey import ValkeyStore
from starlette.requests import Request
from starlette.responses import JSONResponse

from settings import settings
from middlewares import CredentialMiddleware
from services.api import APIService
from services.database import DatabaseService

logger = get_logger(__name__)

# Create JWT verifier for authentication
jwt_verifier = JWTVerifier(
    public_key=settings.JWT_SIGNING_KEY,
    issuer="fastmcp-test",
    audience="fastmcp-credential-demo",
    algorithm="HS256",
)

# Initialize FastMCP server with authentication
mcp = FastMCP("fastmcp-test", auth=jwt_verifier)

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


@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request):
    """Health check endpoint for Docker health checks"""
    return JSONResponse(content={"status": "healthy", "server": "fastmcp-test"})


def main():
    """Main entry point for the FastMCP server"""
    mcp.run(transport="http", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
