# src/handlers/course/course_info.py

from telebot.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from src.common import bot
from src.states import get_state, UserState
from src.texts.course import ONLINE_GROUP_CLASS_DESC
from src.config import COURSE_PAY_LINK

@bot.callback_query_handler(
    func=lambda c: c.data == "course_info"
    and get_state(c.from_user.id) == UserState.COURSE_PAY
)
async def course_info(callback: CallbackQuery):
    await bot.answer_callback_query(callback.id)

    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(
        "Оплатить и начать заниматься",
        url=COURSE_PAY_LINK
    ))
    kb.add(InlineKeyboardButton(
        "Пройти пробный урок",
        callback_data="flow_trial"
    ))
    kb.add(InlineKeyboardButton(
        "🔙 Назад",
        callback_data="back_formats"
    ))

    await bot.send_message(
        callback.message.chat.id,
        ONLINE_GROUP_CLASS_DESC,
        reply_markup=kb
    )
