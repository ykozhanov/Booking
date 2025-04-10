from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    DEBUG: bool = False
    DATABASE_URL: str = "postgresql+asyncpg://user:password@db/restaurant"
    DATABASE_TEST_URL: str = (
        "postgresql+asyncpg://user:password@localhost/test_restaurant"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings():
    return Settings()
