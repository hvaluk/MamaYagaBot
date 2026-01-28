# src/handlers/course/trial/trial_send.py

import asyncio
from telebot.types import CallbackQuery
from src.common import bot
from src.keyboards.inline_kb import trial_lesson_kb, followup_60min_kb, followup_24h_kb
from src.texts.common import TRIAL_OFFER, FOLLOWUP_FIRST, FOLLOWUP_24H
from src.utils.followup import schedule_followup

@bot.callback_query_handler(func=lambda c: c.data == "flow_trial")
async def trial_lesson(callback: CallbackQuery):
    await bot.answer_callback_query(callback.id)

    user_id = callback.from_user.id
    chat_id = callback.message.chat.id

    # Отправляем пробный урок
    await bot.send_message(
        chat_id,
        TRIAL_OFFER,
        reply_markup=trial_lesson_kb()
    )

    # Follow-up через 60 минут
    asyncio.create_task(schedule_followup(
        user_id=user_id,
        text=FOLLOWUP_FIRST,
        kb=followup_60min_kb(),
        delay_seconds=60 * 60
    ))

    # Follow-up через 24 часа
    asyncio.create_task(schedule_followup(
        user_id=user_id,
        text=FOLLOWUP_24H,
        kb=followup_24h_kb(),
        delay_seconds=24 * 60 * 60
    ))

