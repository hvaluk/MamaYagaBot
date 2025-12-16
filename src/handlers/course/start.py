# src/handlers/course/start.py 

from telebot.types import CallbackQuery
from src.common import bot
from src.keyboards.inline_kb import pregnancy_kb
from src.texts.common import ASK_TERM

@bot.callback_query_handler(func=lambda c: c.data == "flow_course")
async def start_course_flow(callback: CallbackQuery):
    """Начало курса — спрашиваем срок беременности"""
    await bot.send_message(
        callback.message.chat.id,
        ASK_TERM,
        reply_markup=pregnancy_kb()
    )
