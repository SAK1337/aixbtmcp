"""Configuration management with Pydantic Settings."""

from functools import lru_cache
from typing import Optional

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration with validation."""

    # Required - AIXBT API
    aixbt_api_key: SecretStr = Field(
        ...,
        description="AIXBT API key for REST API access",
    )

    # Optional - x402 support
    evm_private_key: Optional[SecretStr] = Field(
        default=None,
        description="EVM private key for x402 payments",
    )
    base_rpc_url: str = Field(
        default="https://mainnet.base.org",
        description="Base chain RPC endpoint",
    )

    # Server settings
    host: str = Field(default="127.0.0.1")
    port: int = Field(default=8000, ge=1, le=65535)
    debug: bool = Field(default=False)

    # Rate limiting
    rate_limit_per_minute: int = Field(default=100, ge=1)
    rate_limit_per_day: int = Field(default=100000, ge=1)

    # Caching
    cache_ttl_seconds: int = Field(default=300, ge=0)  # 5 minutes

    # x402 budget controls
    max_price_per_call_usdc: float = Field(default=1.0, ge=0)
    max_spend_per_day_usdc: float = Field(default=10.0, ge=0)

    # Logging
    log_level: str = Field(default="INFO")
    log_format: str = Field(default="json")  # "json" or "text"

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        valid = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid:
            raise ValueError(f"log_level must be one of {valid}")
        return v.upper()

    @field_validator("log_format")
    @classmethod
    def validate_log_format(cls, v: str) -> str:
        valid = ["json", "text"]
        if v.lower() not in valid:
            raise ValueError(f"log_format must be one of {valid}")
        return v.lower()

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
    }


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
