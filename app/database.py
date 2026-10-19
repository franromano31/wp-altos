from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

from app.config import settings


engine = create_async_engine(
    settings.database_url,
    pool_pre_ping=True,
)


async def check_database():
    async with engine.connect() as connection:
        result = await connection.execute(text("SELECT 1"))
        return result.scalar_one()
