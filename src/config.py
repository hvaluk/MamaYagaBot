import os
from dotenv import load_dotenv
from pyairtable import Table

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

# --- Airtable setup ---
AIRTABLE_TOKEN = os.getenv("AIRTABLE_TOKEN")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_SETTINGS_TABLE = os.getenv("AIRTABLE_SETTINGS_TABLE", "Settings")

if not AIRTABLE_TOKEN or not AIRTABLE_BASE_ID:
    print("⚠️ Airtable keys not set in .env, using .env fallback for dynamic settings.")
    AIRTABLE_ENABLED = False
else:
    AIRTABLE_ENABLED = True

def load_airtable_settings():
    """Load settings from Airtable table, return dict {key: value}"""
    if not AIRTABLE_ENABLED:
        return {}
    try:
        table = Table(AIRTABLE_TOKEN, AIRTABLE_BASE_ID, AIRTABLE_SETTINGS_TABLE)
        return {r['fields']['key']: r['fields']['value'] for r in table.all()}
    except Exception as e:
        print(f"⚠️ Warning: cannot load settings from Airtable: {e}")
        return {}

AIRTABLE_SETTINGS = load_airtable_settings()

def get_setting(key, default=""):
    """
    Return value from Airtable if available, else from .env, else default
    """
    return AIRTABLE_SETTINGS.get(key, os.getenv(key, default))

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
FOLLOWUP_CHECK_INTERVAL = int(get_setting("FOLLOWUP_CHECK_INTERVAL", "10"))

# --- Summary for logs ---
if AIRTABLE_ENABLED:
    print("Airtable settings loaded successfully.")
else:
    print("Using .env fallback values only.")
