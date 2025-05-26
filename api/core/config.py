from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://quant_user:quant_password@postgres:5432/quant_db"
    alpha_vantage_api_key: str = "demo"
    postgres_db: str = "quant_db"
    postgres_user: str = "quant_user"
    postgres_password: str = "quant_password"

    class Config:
        env_file = ".env"
        extra = "allow"


@lru_cache
def get_settings() -> Settings:
    return Settings()
