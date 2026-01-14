# src/handlers/course/contra.py

from telebot.types import CallbackQuery
from src.common import bot
from src.dao.models import AsyncSessionLocal, User, Request
from src.keyboards.inline_kb import formats_kb, leave_contact_kb
from src.texts.common import CONTRA_TEXT, SAFE_TEXT, FORMAT_TEXT
from src.states import get_state, set_state, clear_state, UserState

@bot.callback_query_handler(
    func=lambda c: c.data.startswith("contra_") or c.data == "leave_contact"
)
async def course_contra(callback: CallbackQuery):
    user_id = callback.from_user.id

    async with AsyncSessionLocal() as session:
        user = await session.get(User, user_id)
        if not user:
            return

        if callback.data.startswith("contra_"):
            user.contraindications = callback.data
            session.add(Request(user_id=user.telegram_id, request_type="contraindications", payload=callback.data))
            await session.commit()

            if callback.data != "contra_ok":
                # Если есть противопоказания — просим оставить контакт
                set_state(user_id, UserState.COURSE_CONTACT)
                await bot.send_message(callback.message.chat.id, CONTRA_TEXT, reply_markup=leave_contact_kb())
            else:
                set_state(user_id, UserState.COURSE_FORMAT)
                await bot.send_message(callback.message.chat.id, SAFE_TEXT)
                await bot.send_message(callback.message.chat.id, FORMAT_TEXT, reply_markup=formats_kb())

        elif callback.data == "leave_contact":
            # Проверяем, что юзер в нужном состоянии
            if get_state(user_id) != UserState.COURSE_CONTACT:
                return

            phone = user.phone or "не указан"
            session.add(Request(user_id=user.telegram_id, request_type="contact", payload=phone))
            await session.commit()

            clear_state(user_id)
            await bot.send_message(callback.message.chat.id, "Спасибо! 💛 Анна скоро свяжется с вами.")
