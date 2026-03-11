# src/handlers/course/trial/remind_later.py

from datetime import datetime, timezone
from telebot.types import CallbackQuery
from sqlalchemy import select

from src.common import bot
from src.dao.models import AsyncSessionLocal, Application


async def get_last_app(session, user_id: int):
    stmt = select(Application).where(Application.user_id == user_id).order_by(Application.id.desc()).limit(1)
    result = await session.execute(stmt)
    return result.scalars().first()


@bot.callback_query_handler(func=lambda c: c.data == "remind_later")
async def remind_later(callback: CallbackQuery):
    """User requested to be reminded later in 3 days."""
    await bot.answer_callback_query(callback.id, "Хорошо, напомню через 3 дня 🕒")
    user_id = callback.from_user.id

    async with AsyncSessionLocal() as session:
        app = await get_last_app(session, user_id)
        if not app or app.followup_stage >= 99:
            return

        # Mark application as "remind later" — handled by followup_worker
        app.followup_stage = 3
        app.followup_last_sent_at = datetime.now(timezone.utc)
        await session.commit()
