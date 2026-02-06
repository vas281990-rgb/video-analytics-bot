from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
from app.config.settings import settings

# Load environment variables from .env
load_dotenv()

# Build DATABASE_URL from settings
DATABASE_URL = (
    f"postgresql+asyncpg://{settings.DB_USER}:"
    f"{settings.DB_PASSWORD}@{settings.DB_HOST}:"
    f"{settings.DB_PORT}/{settings.DB_NAME}"
)

# Async SQLAlchemy engine
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
)

# Factory for async DB sessions
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncSession:
    """
    Dependency that provides an async DB session
    """
    async with AsyncSessionLocal() as session:
        yield session
