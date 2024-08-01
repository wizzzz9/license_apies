from typing import Any, List
from pydantic import PostgresDsn, RedisDsn, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.constants import Environment


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


    REDIS_URL: str = ""
    ENVIRONMENT: Environment = Environment.PRODUCTION
    # SENTRY_DSN: str = None
    CORS_ORIGINS: List[str] = list()
    CORS_ORIGINS_REGEX: str | None = None
    CORS_HEADERS: List[str] = list()

    APP_VERSION: str = "1"

    DB_HOST: str
    DB_PORT: str = "5432"
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    DB_TYPE: str = "postgres"

    class Config:
        env_file = '.env'
        extra = 'ignore'
    # @model_validator(mode="after")
    # def validate_sentry_non_local(self) -> "Config":
    #     if self.ENVIRONMENT.is_deployed and not self.SENTRY_DSN:
    #         raise ValueError("Sentry is not set")
    #
    #     return self






settings = Config()
DATABASE_URL: str = (f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@"
                     f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}?async_fallback=True")
