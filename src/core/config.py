import logging
from datetime import datetime
from logging.config import DictConfigurator
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)


def configure_logging():
    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            },
            "json": {
                "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                "format": """
                    asctime: %(asctime)s
                    level: %(levelname)s
                    name: %(name)s
                    message: %(message)s
                    pathname: %(pathname)s
                    funcName: %(funcName)s
                    lineno: %(lineno)d
                    traceback: %(exc_info)s
                """,
            },
        },
        "handlers": {
            "file": {
                "class": "logging.handlers.ConcurrentRotatingFileHandler",
                "filename": LOG_DIR / f"app_{datetime.now().strftime('%Y-%m-%d')}.log",
                "maxBytes": 1024 * 1024 * 10,
                "backupCount": 5,
                "formatter": "json",
                "encoding": "utf-8",
                "delay": True,
            },
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "simple",
                "level": "DEBUG",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "app": {
                "handlers": ["file", "console"],
                "level": "INFO",
                "propagate": False,
            },
            "app.debug": {
                "handlers": ["console"],
                "level": "DEBUG",
                "propagate": False,
            },
        },
        "root": {"handlers": ["console"], "level": "WARNING"},
    }

    DictConfigurator(log_config)


configure_logging()
logger = logging.getLogger("app")


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
