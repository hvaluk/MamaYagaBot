# src/handlers/course/contra.py

from telebot.types import CallbackQuery
from src.common import bot
from src.dao.models import AsyncSessionLocal, User, Request
from src.keyboards.inline_kb import formats_kb, leave_contact_kb
from src.texts.common import CONTRA_TEXT, FORMAT_TEXT
from src.states import UserState

@bot.callback_query_handler(func=lambda c: c.data.startswith("contra_"))
async def save_contra(callback: CallbackQuery):
    """Сохраняем противопоказания и, если нужно, запрашиваем контакт"""
    async with AsyncSessionLocal() as session:
        user = await session.get(User, callback.from_user.id)
        if not user:
            return

        user.contraindications = callback.data
        if callback.data != "contra_ok":
            user.state = UserState.WAITING_CONTACT

        session.add_all([
            user,
            Request(
                user_id=user.telegram_id,
                request_type="contraindications",
                payload=callback.data
            )
        ])
        await session.commit()

    if callback.data != "contra_ok":
        await bot.send_message(
            callback.message.chat.id,
            CONTRA_TEXT,
            reply_markup=leave_contact_kb()
        )
        return

    await bot.send_message(
        callback.message.chat.id,
        FORMAT_TEXT,
        reply_markup=formats_kb()
    )
