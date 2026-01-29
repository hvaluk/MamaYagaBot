# src/handlers/course/trial/trial_send.py

from telebot.types import CallbackQuery
from datetime import datetime
from sqlalchemy import select

from src.common import bot
from src.dao.models import AsyncSessionLocal, Application
from src.keyboards.inline_kb import trial_lesson_kb
from src.texts.common import TRIAL_OFFER


def utcnow():
    return datetime.utcnow()


@bot.callback_query_handler(func=lambda c: c.data == "flow_trial")
async def trial_lesson(callback: CallbackQuery):
    await bot.answer_callback_query(callback.id)

    user_id = callback.from_user.id
    chat_id = callback.message.chat.id

    await bot.send_message(chat_id, TRIAL_OFFER, reply_markup=trial_lesson_kb())

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Application)
            .where(Application.user_id == user_id)
            .order_by(Application.created_at.desc())
        )
        app = result.scalars().first()
        if app:
            app.is_trial = True
            app.trial_opened_at = utcnow()
            app.followup_stage = 0
            app.followup_last_sent_at = None
            await session.commit()
