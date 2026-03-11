# config.py 

import os
from dotenv import load_dotenv
import requests


load_dotenv()

# --- Telegram ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TELEGRAM_TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN not set in .env")

def parse_ids(ids_str: str):
    """Parse comma-separated string into a set of integers"""
    return set(int(x) for x in ids_str.split(",") if x.strip())

ADMIN_IDS = parse_ids(os.getenv("ADMIN_IDS", ""))
OWNER_IDS = parse_ids(os.getenv("OWNER_IDS", ""))

# --- Database ---
DATABASE_URL = os.getenv("MAMAYOGA_DATABASE_URL", "sqlite+aiosqlite:///mamayoga_bot.db")

# --- NocoDB setup ---

NOCODB_URL = os.getenv("NOCODB_URL")
NOCODB_TOKEN = os.getenv("NOCODB_TOKEN")
NOCODB_TABLE_ID = os.getenv("NOCODB_TABLE_ID")

if not NOCODB_URL or not NOCODB_TOKEN or not NOCODB_TABLE_ID:
    print("⚠️ NocoDB keys not set in .env, using .env fallback.")
    NOCODB_ENABLED = False
else:
    NOCODB_ENABLED = True


def load_nocodb_settings():
    """Load settings from NocoDB table → dict {key: value}"""

    if not NOCODB_ENABLED:
        return {}

    url = f"{NOCODB_URL}/api/v2/tables/{NOCODB_TABLE_ID}/records?limit=1000"

    headers = {
        "xc-token": NOCODB_TOKEN
    }

    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()

        data = r.json()["list"]

        return {row["key"]: row["value"] for row in data}

    except Exception as e:
        print(f"⚠️ Warning: cannot load settings from NocoDB: {e}")
        return {}


NOCODB_SETTINGS = load_nocodb_settings()


def get_setting(key, default=""):
    """
    Return value from NocoDB if available,
    else from .env,
    else default
    """
    return NOCODB_SETTINGS.get(key, os.getenv(key, default))


def parse_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default
    
# --- Links ---
PAY_LINK = get_setting("PAY_LINK")
TRIAL_MINI_COURSE = get_setting("TRIAL_MINI_COURSE")
SITE = get_setting("SITE")
COURSE_PAY_LINK = get_setting("COURSE_PAY_LINK")

# --- Prices ---
ONLINE_GROUP_PRICE_BYN = parse_int(get_setting("ONLINE_GROUP_PRICE_BYN"))
ONLINE_GROUP_PRICE_EUR = parse_int(get_setting("ONLINE_GROUP_PRICE_EUR"))
COURSE_PRICE_BYN = parse_int(get_setting("COURSE_PRICE_BYN"))
COURSE_PRICE_EUR = parse_int(get_setting("COURSE_PRICE_EUR"))
SINGLE_CLASS_PRICE_BYN = parse_int(get_setting("SINGLE_CLASS_PRICE_BYN"))
SINGLE_CLASS_PRICE_EUR = parse_int(get_setting("SINGLE_CLASS_PRICE_EUR"))
INDIVIDUAL_CLASS_PRICE_BYN = parse_int(get_setting("INDIVIDUAL_CLASS_PRICE_BYN"))
INDIVIDUAL_CLASS_PRICE_EUR = parse_int(get_setting("INDIVIDUAL_CLASS_PRICE_EUR"))
SUBSCRIPTION_4_CLASSES_PRICE_BYN = parse_int(get_setting("SUBSCRIPTION_4_CLASSES_PRICE_BYN"))
SUBSCRIPTION_4_CLASSES_PRICE_EUR = parse_int(get_setting("SUBSCRIPTION_4_CLASSES_PRICE_EUR"))
SUBSCRIPTION_8_CLASSES_PRICE_BYN = parse_int(get_setting("SUBSCRIPTION_8_CLASSES_PRICE_BYN"))
SUBSCRIPTION_8_CLASSES_PRICE_EUR = parse_int(get_setting("SUBSCRIPTION_8_CLASSES_PRICE_EUR"))

# --- Worker ---
FOLLOWUP_CHECK_INTERVAL = parse_int(get_setting("FOLLOWUP_CHECK_INTERVAL"))

# --- Summary for logs ---
if NOCODB_ENABLED:
    print("NocoDB settings loaded successfully.")
else:
    print("Using .env fallback values only.")

