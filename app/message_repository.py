
from sqlalchemy import update, func
from sqlalchemy.dialects.postgresql import insert

from app.database import SessionLocal
from app.models import Message


async def save_message(message_id: str, phone: str, content: str) -> bool:
    async with SessionLocal() as session:
        statement = (
            insert(Message)
            .values(
                id=message_id,
                phone=phone,
                content=content,
                status="pending",
            )
            .on_conflict_do_nothing(index_elements=["id"])
            .returning(Message.id)
        )

        result = await session.execute(statement)
        inserted_id = result.scalar_one_or_none()

        await session.commit()

        return inserted_id is not None


async def mark_processing(message_id: str):
    async with SessionLocal() as session:
        await session.execute(
            update(Message)
            .where(Message.id == message_id)
            .values(
                status="processing",
                attempts=Message.attempts + 1,
                updated_at=func.now(),
            )
        )
        await session.commit()


async def save_response(message_id: str, answer: str):
    async with SessionLocal() as session:
        await session.execute(
            update(Message)
            .where(Message.id == message_id)
            .values(
                response=answer,
                updated_at=func.now(),
            )
        )
        await session.commit()


async def finish_message(message_id: str, status: str):
    async with SessionLocal() as session:
        await session.execute(
            update(Message)
            .where(Message.id == message_id)
            .values(
                status=status,
                updated_at=func.now(),
            )
        )
        await session.commit()
