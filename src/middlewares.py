"""
Simplified credential middleware using on_call_tool hook
"""

from typing import Any, Dict
from cryptography.fernet import Fernet
from fastmcp.server.dependencies import get_access_token, AccessToken
from fastmcp.server.middleware import Middleware, MiddlewareContext, CallNext
from fastmcp.utilities.logging import get_logger
from key_value.aio.stores.valkey import ValkeyStore
from key_value.aio.wrappers.encryption import FernetEncryptionWrapper

from settings import settings

logger = get_logger(__name__)


def get_mock_credentials() -> Dict[str, Any]:
    """Get mock credentials for all services"""
    return {
        "api_service": {
            "url": "https://api.example.com",
            "token": "demo-token-123456789",
            "timeout": 30,
        },
        "database": {
            "url": "postgresql://user:password@localhost:5432/dbname",
            "pool_size": 10,
        },
    }


class CredentialMiddleware(Middleware):
    """
    Simplified credential middleware that only handles credential injection
    for tools that need it. Uses on_call_tool hook for better performance.
    """

    def __init__(self, valkey_store: ValkeyStore):
        """Initialize the credential middleware"""
        # Add encryption wrapper
        self.credential_store = FernetEncryptionWrapper(
            key_value=valkey_store, fernet=Fernet(settings.ENCRYPTION_KEY.encode())
        )

    async def on_call_tool(
        self, context: MiddlewareContext, call_next: CallNext
    ) -> Any:
        """
        Handle tool calls - inject credentials if needed
        """
        # Extract customer_id from JWT token
        customer_id = self._extract_customer_id_from_context()

        # All tools require credentials based on customer_id
        credentials = await self._get_tool_credentials(customer_id)
        if credentials:
            # Store credentials in context state using set_state method
            context.fastmcp_context.set_state("_credentials", credentials)
            logger.info(
                f"Injected credentials into context for customer: {customer_id}"
            )

        return await call_next(context)

    def _extract_customer_id_from_context(self) -> str:
        """Extract customer_id using FastMCP's access token system"""
        # Use FastMCP's proper access token system
        token: AccessToken | None = get_access_token()

        if token is None:
            raise ValueError("No access token found")

        # Extract customer_id from JWT claims
        customer_id = token.claims.get("customer_id")
        if not customer_id:
            # Try standard JWT subject claim as fallback
            customer_id = token.claims.get("sub")

        return customer_id

    async def _get_tool_credentials(self, customer_id: str) -> Dict[str, Any]:
        """Retrieve credentials for a specific tool"""
        credential_key = f"customer:{customer_id}"
        stored_credentials = await self.credential_store.get(credential_key)

        if stored_credentials:
            logger.info(f"Retrieved stored credentials for customer {customer_id}")
            return stored_credentials

        return get_mock_credentials()
