# src/config.py
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TELEGRAM_TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN not set in .env")


# ADMIN_IDS and OWNER_IDS parsing helper
def parse_ids(ids_str: str):
    return set(int(x) for x in ids_str.split(",") if x.strip())

ADMIN_IDS = parse_ids(os.getenv("ADMIN_IDS", ""))
OWNER_IDS = parse_ids(os.getenv("OWNER_IDS", ""))


# --- Database ---
DATABASE_URL = os.getenv("MAMAYOGA_DATABASE_URL", "sqlite+aiosqlite:///mamayoga_bot.db")

# --- Links & Course ---
PAY_LINK = os.getenv("PAY_LINK", "")

TRIAL_MINI_COURSE = os.getenv("TRIAL_MINI_COURSE", "")
SITE = os.getenv("SITE", "")
COURSE_PAY_LINK = os.getenv("COURSE_PAY_LINK", "")

   
# --- Course Prices ---
def parse_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default

ONLINE_GROUP_PRICE_BYN = parse_int(os.getenv("ONLINE_GROUP_PRICE_BYN", ""))
ONLINE_GROUP_PRICE_EUR = parse_int(os.getenv("ONLINE_GROUP_PRICE_EUR", ""))

COURSE_PRICE_BYN = parse_int(os.getenv("COURSE_PRICE_BYN", ""))
COURSE_PRICE_EUR = parse_int(os.getenv("COURSE_PRICE_EUR", ""))

SINGLE_CLASS_PRICE_BYN = parse_int(os.getenv("SINGLE_CLASS_PRICE_BYN", ""))
SINGLE_CLASS_PRICE_EUR = parse_int(os.getenv("SINGLE_CLASS_PRICE_EUR", ""))

INDIVIDUAL_CLASS_PRICE_BYN = parse_int(os.getenv("INDIVIDUAL_CLASS_PRICE_BYN", ""))
INDIVIDUAL_CLASS_PRICE_EUR = parse_int(os.getenv("INDIVIDUAL_CLASS_PRICE_EUR", ""))

SUBSCRIPTION_4_CLASSES_PRICE_BYN = parse_int(os.getenv("SUBSCRIPTION_4_CLASSES_PRICE_BYN", ""))
SUBSCRIPTION_4_CLASSES_PRICE_EUR = parse_int(os.getenv("SUBSCRIPTION_4_CLASSES_PRICE_EUR", ""))

SUBSCRIPTION_8_CLASSES_PRICE_BYN = parse_int(os.getenv("SUBSCRIPTION_8_CLASSES_PRICE_BYN", ""))
SUBSCRIPTION_8_CLASSES_PRICE_EUR = parse_int(os.getenv("SUBSCRIPTION_8_CLASSES_PRICE_EUR", ""))


# --- Worker ---
FOLLOWUP_CHECK_INTERVAL = int(os.getenv("FOLLOWUP_CHECK_INTERVAL", "10"))