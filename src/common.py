# src/common.py

from telebot.async_telebot import AsyncTeleBot
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

bot = AsyncTeleBot(TOKEN)

