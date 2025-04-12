from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from src.core.config import get_settings

settings = get_settings()

engine = create_async_engine(
    settings.get_database_url(),
    echo=settings.DEBUG,
    connect_args={
        "server_settings": {
            "timezone": "UTC",
        }
    }
)

AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session
