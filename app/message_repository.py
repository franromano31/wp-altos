from sqlalchemy import update, func
from sqlalchemy.dialects.postgresql import insert

from app.database import SessionLocal
from app.models import Message

from datetime import datetime, timedelta, timezone
from sqlalchemy import select


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

async def get_conversation_history(phone: str, limit: int = 10):
    since = datetime.now(timezone.utc) - timedelta(hours=24)

    async with SessionLocal() as session:
        result = await session.execute(
            select(Message)
            .where(
                Message.phone == phone,
                Message.status == "sent",
                Message.created_at >= since,
            )
            .order_by(Message.created_at.desc(), Message.id.desc())
            .limit(limit)
        )

        messages = list(reversed(result.scalars().all()))

    history = []

    for message in messages:
        history.append({
            "role": "user",
            "content": message.content,
        })

        if message.response:
            history.append({
                "role": "assistant",
                "content": message.response,
            })

    return history
