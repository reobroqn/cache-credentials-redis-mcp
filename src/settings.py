"""
Simple configuration using environment variables
"""

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings using environment variables"""

    # Redis Configuration - Individual connection parameters
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    # Encryption Configuration
    ENCRYPTION_KEY: str = "your-fernet-encryption-key-here-32-bytes"

    # Server Configuration
    SERVER_NAME: str = "fastmcp-credential-demo"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    @field_validator("ENCRYPTION_KEY")
    @classmethod
    def validate_encryption_key(cls, v: str) -> str:
        """Validate that the encryption key is properly formatted for Fernet"""
        try:
            from cryptography.fernet import Fernet

            Fernet(v.encode())
            return v
        except Exception as e:
            raise ValueError(f"Invalid encryption key: {e}")


# Global settings instance
settings = Settings()
