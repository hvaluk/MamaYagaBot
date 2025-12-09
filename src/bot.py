# src/bot.py
import aiohttp
from telebot.async_telebot import AsyncTeleBot
from telebot import types
from src.config import TELEGRAM_TOKEN


bot = AsyncTeleBot(TELEGRAM_TOKEN)


# import handlers (they will register handlers with the bot)
from src.handlers import start, flow_pregnancy, flow_experience, flow_contra, flow_formats, booking, admin


async def start_polling():
    await bot.polling(non_stop=True)