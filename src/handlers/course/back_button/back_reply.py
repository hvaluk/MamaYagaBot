# src/handlers/course/back_button/back_reply.py

from telebot.types import Message
from src.common import bot
from src.handlers.course.back import handle_back


@bot.message_handler(func=lambda m: m.text == "Назад")
async def back_reply(message: Message):
    await handle_back(message.from_user.id, message.chat.id)
