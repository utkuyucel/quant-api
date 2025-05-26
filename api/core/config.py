from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables or .env file.
    All sensitive values must be provided via environment configuration.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="allow",
        case_sensitive=False
    )

    # Database configuration - NO DEFAULTS for security
    database_url: str
    postgres_db: str
    postgres_user: str
    postgres_password: str

    # API keys - NO DEFAULTS for security
    alpha_vantage_api_key: str

    # Optional application settings with safe defaults
    app_name: str = "Quant API - Bitcoin Analysis Platform"
    app_version: str = "1.0.0"
    debug: bool = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
