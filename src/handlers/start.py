# src/handlers/start.py

from src.bot import bot
from src.keyboards.inline_kb import main_kb
from src.services.users import ensure_user

@bot.message_handler(commands=['start'])
async def start(message):
    await ensure_user(message.from_user)
    kb = main_kb()
    text = (
        "Привет! Я помощник Анны. Помогу тебе хорошо чувствовать себя "
        "во время беременности и подготовиться к родам.\n\nС чего начнём?"
    )
    await bot.send_message(message.chat.id, text, reply_markup=kb)
