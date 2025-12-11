# src/config.py
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TELEGRAM_TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN not set in .env")

ADMIN_IDS = set(int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip())

DATABASE_URL = os.getenv("MAMAYOGA_DATABASE_URL", "sqlite+aiosqlite:///mamayoga_bot.db")

PAY_LINK = os.getenv("PAY_LINK")
TRIAL_VIDEO = os.getenv("TRIAL_VIDEO")
TRIAL_LECT = os.getenv("TRIAL_LECT")
SITE = os.getenv("SITE")

# FOLLOWUP_CHECK_INTERVAL = int(os.getenv("FOLLOWUP_CHECK_INTERVAL", "60"))