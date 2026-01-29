# src/handlers/course/trial/remind_later.py

import asyncio
from datetime import datetime, timezone
from telebot.types import CallbackQuery
from sqlalchemy import select

from src.common import bot
from src.dao.models import AsyncSessionLocal, Application
from src.texts.common import FOLLOWUP_3D
from src.keyboards.inline_kb import followup_3days_kb


async def get_last_app(session, user_id: int):
    stmt = select(Application).where(Application.user_id == user_id).order_by(Application.id.desc()).limit(1)
    result = await session.execute(stmt)
    return result.scalars().first()


@bot.callback_query_handler(func=lambda c: c.data == "remind_later")
async def remind_later(callback: CallbackQuery):
    await bot.answer_callback_query(callback.id, "Хорошо, напомню через 3 дня 🕒")
    user_id = callback.from_user.id

    async with AsyncSessionLocal() as session:
        app = await get_last_app(session, user_id)
        if not app or app.followup_stage >= 99:
            return

        # Помечаем заявку, что пользователь попросил "напомнить позже"
        app.followup_stage = 3
        app.followup_last_sent_at = datetime.now(timezone.utc)
        await session.commit()

    # Асинхронная отправка через delay
    async def send_later(user_id: int, name: str = ""):
        # ===== ТЕСТ: через 3 минуты =====
        await asyncio.sleep(180)  
        # ===== ПРОДАКШН: через 3 дня =====
        # await asyncio.sleep(3 * 24 * 60 * 60)

        # Отправляем follow-up сообщение с клавиатурой
        await bot.send_message(
            user_id,
            text=FOLLOWUP_3D.format(name=callback.from_user.first_name),
            reply_markup=followup_3days_kb()
        )

        # Обновляем статус follow-up
        async with AsyncSessionLocal() as s:
            a = await s.get(Application, app.id)
            if a:
                a.followup_stage = 99
                await s.commit()

    asyncio.create_task(send_later(user_id))
