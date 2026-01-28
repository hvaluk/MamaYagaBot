# src/handlers/course/trial/remind_later.py

import asyncio
from telebot.types import CallbackQuery
from sqlalchemy import select

from src.common import bot
from src.dao.models import AsyncSessionLocal, Application
from src.texts.common import FOLLOWUP_24H
from src.keyboards.inline_kb import followup_24h_kb


@bot.callback_query_handler(func=lambda c: c.data == "remind_later")
async def remind_later(callback: CallbackQuery):
    await bot.answer_callback_query(callback.id, "Хорошо, напомню через 3 дня 🕒")

    user_id = callback.from_user.id

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Application)
            .where(Application.user_id == user_id)
            .order_by(Application.created_at.desc())
        )
        app = result.scalars().first()

        if not app or not app.followup_2_sent:
            return

        async def last_ping():
            await asyncio.sleep(3 * 24 * 60 * 60)
            await bot.send_message(user_id, FOLLOWUP_24H, reply_markup=followup_24h_kb())

            async with AsyncSessionLocal() as s:
                a = await s.get(Application, app.id)
                if a:
                    a.status = "done"
                    await s.commit()

        asyncio.create_task(last_ping())
