from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)

from app.config import settings


engine = create_async_engine(
    settings.database_url,
    pool_pre_ping=True,
)

SessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
)



async def check_database():
    async with engine.connect() as connection:
        result = await connection.execute(text("SELECT 1"))
        return result.scalar_one()
