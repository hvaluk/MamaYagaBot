# src/handlers/course/back_button/back_inline.py

from telebot.types import CallbackQuery
from src.common import bot
from src.handlers.course.back import handle_back

@bot.callback_query_handler(func=lambda c: c.data == "back")
async def back_inline(callback: CallbackQuery):
    await bot.answer_callback_query(callback.id)
    await handle_back(callback.from_user.id, callback.message.chat.id)