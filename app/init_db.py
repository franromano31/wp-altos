import asyncio

from app.database import engine
from app.models import Base


async def main():
    try:
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

        print("Tablas creadas correctamente")

    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
