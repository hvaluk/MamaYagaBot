# src/common.py

import os
from telebot.async_telebot import AsyncTeleBot
from dotenv import load_dotenv

load_dotenv()

# --- BOT INITIALIZATION ---

TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TOKEN:
    raise ValueError("❌ TELEGRAM_TOKEN is not set")

bot = AsyncTeleBot(
    TOKEN,
    parse_mode="HTML"  # ✅ safer for formatting than Markdown
)