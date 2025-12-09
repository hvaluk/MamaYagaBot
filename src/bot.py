# src/bot.py

from telebot.async_telebot import AsyncTeleBot
from src.config import TELEGRAM_TOKEN

bot = AsyncTeleBot(TELEGRAM_TOKEN)

# Импорт хендлеров
from src.handlers import start, flow_pregnancy, flow_experience, flow_contra, flow_formats, booking, followup, admin

async def start_polling():
    await bot.polling(non_stop=True)
