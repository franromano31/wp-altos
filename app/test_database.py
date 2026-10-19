
import asyncio

from app.database import check_database, engine


async def main():
    try:
        result = await check_database()
        print("PostgreSQL conectado:", result)
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
