from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    DEBUG: bool = False
    DATABASE_TEST_URL: str = "sqlite+aiosqlite:///:memory"
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    def get_database_url(self, host: str | None = None) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{host or self.POSTGRES_HOST}:{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )


@lru_cache
def get_settings():
    return Settings()
