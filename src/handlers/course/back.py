# src/handlers/course/back.py

from telebot.types import CallbackQuery
from src.common import bot
from src.states import set_state, get_state, UserState
from src.keyboards.inline_kb import formats_kb

@bot.callback_query_handler(
    func=lambda c: c.data == "back_formats"
    and get_state(c.from_user.id) in (UserState.COURSE_PAY, UserState.COURSE_CONTACT)
)
async def back_to_formats(callback: CallbackQuery):
    await bot.answer_callback_query(callback.id)
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id

    set_state(user_id, UserState.COURSE_FORMAT)
    await bot.send_message(chat_id, "Выбери формат занятий:", reply_markup=formats_kb())
