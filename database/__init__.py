# Database initialization

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
from database.models import Base
import logging

logger = logging.getLogger(__name__)

# Конвертируем URL для async
if DATABASE_URL.startswith("sqlite"):
    async_db_url = DATABASE_URL.replace("sqlite:///", "sqlite+aiosqlite:///")
elif DATABASE_URL.startswith("postgresql"):
    async_db_url = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
else:
    async_db_url = DATABASE_URL

# Создаем async engine
engine = create_async_engine(
    async_db_url,
    echo=False,
    future=True,
)

# Создаем фабрику сессий
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def init_db():
    """Инициализация базы данных"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database initialized")


async def get_session() -> AsyncSession:
    """Получить сессию базы данных"""
    async with AsyncSessionLocal() as session:
        yield session
