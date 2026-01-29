# src/handlers/course/trial/trial_material.py

from datetime import datetime, timezone
from sqlalchemy import select
from telebot.types import CallbackQuery

from src.common import bot
from src.config import TRIAL_MINI_COURSE
from src.dao.models import AsyncSessionLocal, Application

@bot.callback_query_handler(func=lambda c: c.data == "trial_lect")
async def open_trial_material(callback: CallbackQuery):
    await bot.answer_callback_query(callback.id)

    user_id = callback.from_user.id
    chat_id = callback.message.chat.id

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Application)
            .where(Application.user_id == user_id)
            .order_by(Application.created_at.desc())
        )
        app = result.scalars().first()

        if not app:
            return

        if app.trial_opened_at:
            # уже открыт — просто отправляем ссылку
            await bot.send_message(chat_id, TRIAL_MINI_COURSE)
            return

        # открываем trial впервые
        app.is_trial = True
        app.trial_opened_at = datetime.now(timezone.utc)
        app.followup_stage = 0
        app.followup_last_sent_at = None
        await session.commit()

    await bot.send_message(chat_id, TRIAL_MINI_COURSE)
