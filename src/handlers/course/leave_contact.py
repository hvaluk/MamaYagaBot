# src/handlers/course/leave_contact.py

from telebot.types import CallbackQuery
from src.common import bot
from src.states import set_state, UserState
from src.keyboards.reply_kb import contact_request_kb

@bot.callback_query_handler(func=lambda c: c.data == "leave_contact")
async def ask_contact(callback: CallbackQuery):
    await bot.answer_callback_query(callback.id)

    set_state(callback.from_user.id, UserState.COURSE_CONTACT)

    await bot.send_message(
        callback.message.chat.id,
        "Оставь номер телефона кнопкой ниже или напиши свой Telegram @username",
        reply_markup=contact_request_kb()
    )
