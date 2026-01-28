# src/handlers/course/trial/trial_material.py

import asyncio
from datetime import datetime, timezone
from sqlalchemy import select
from telebot.types import CallbackQuery

from src.common import bot
from src.config import TRIAL_VIDEO, TRIAL_LECT
from src.dao.models import AsyncSessionLocal, Application
from src.utils.followup import schedule_followup


@bot.callback_query_handler(func=lambda c: c.data in ("trial_video", "trial_lect"))
async def open_trial_material(callback: CallbackQuery):
    await bot.answer_callback_query(callback.id)

    user_id = callback.from_user.id
    chat_id = callback.message.chat.id
    url = TRIAL_VIDEO if callback.data == "trial_video" else TRIAL_LECT

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Application)
            .where(Application.user_id == user_id)
            .order_by(Application.created_at.desc())
        )
        application = result.scalars().first()

        if not application:
            return

        # ❗ если уже открывал — просто отдаем ссылку
        if application.trial_opened_at:
            await bot.send_message(chat_id, url)
            return

        application.trial_opened_at = datetime.now(timezone.utc)
        application.is_trial = True
        await session.commit()

    await bot.send_message(chat_id, url)

    asyncio.create_task(
        schedule_followup(user_id, application.id, step=1, delay_seconds=3600)
    )
    asyncio.create_task(
        schedule_followup(user_id, application.id, step=2, delay_seconds=86400)
    )
