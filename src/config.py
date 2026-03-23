# src/config.py

import os
import asyncio
import requests
from dotenv import load_dotenv

load_dotenv()


# --- STATIC ENV SETTINGS ---

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GRIST_API_KEY = os.getenv("GRIST_API_KEY")
GRIST_DOC_ID = os.getenv("GRIST_DOC_ID")
GRIST_BASE_URL = os.getenv("GRIST_URL", "https://grist.hvaluk.de/api/docs/")


def parse_ids(ids_str: str):
    """Parse comma-separated IDs into a set of integers."""
    if not ids_str:
        return set()
    return set(int(x.strip()) for x in ids_str.split(",") if x.strip())


ADMIN_IDS = parse_ids(os.getenv("ADMIN_IDS", ""))
OWNER_IDS = parse_ids(os.getenv("OWNER_IDS", ""))


# --- SETTINGS MANAGER ---

class SettingsManager:
    """
    Central configuration manager.

    Handles:
    - Settings (prices, links)
    - Texts (bot messages)
    - Dynamic formatting
    """

    def __init__(self):
        self._settings: dict = {}
        self._texts: dict = {}
        self.refresh()

    # --- LOAD DATA FROM GRIST ---

    def _refresh_settings(self):
        """Load key-value settings from 'Settings' table."""
        url = f"{GRIST_BASE_URL}{GRIST_DOC_ID}/tables/Settings/records"
        headers = {"Authorization": f"Bearer {GRIST_API_KEY}"}

        try:
            r = requests.get(url, headers=headers, timeout=10)
            r.raise_for_status()
            records = r.json().get("records", [])

            self._settings = {
                rec["fields"]["key"]: rec["fields"]["value"]
                for rec in records
                if "key" in rec["fields"]
            }

            return True

        except Exception as e:
            print(f"⚠️ Settings sync error: {e}")
            return False

    def _refresh_texts(self):
        """Load texts from 'Texts' table."""
        url = f"{GRIST_BASE_URL}{GRIST_DOC_ID}/tables/Texts/records"
        headers = {"Authorization": f"Bearer {GRIST_API_KEY}"}

        try:
            r = requests.get(url, headers=headers, timeout=10)
            r.raise_for_status()
            records = r.json().get("records", [])

            self._texts = {
                rec["fields"]["key"]: rec["fields"]["value"]
                for rec in records
                if "key" in rec["fields"]
            }

            return True

        except Exception as e:
            print(f"⚠️ Texts sync error: {e}")
            return False

    def refresh(self):
        """Refresh both settings and texts."""
        ok_settings = self._refresh_settings()
        ok_texts = self._refresh_texts()
        return ok_settings and ok_texts

    # --- INTERNAL HELPERS ---

    def _get(self, key: str, default=""):
        """Priority: Grist → ENV → default"""
        return self._settings.get(key, os.getenv(key, default))

    def _get_int(self, key: str, default=0):
        """Safely convert value to integer."""
        value = self._get(key, default)
        try:
            return int(float(value))
        except (ValueError, TypeError):
            return default

    def to_dict(self):
        """
        Variables available for text formatting.
        """
        return {
            # --- Prices ---
            "SINGLE_CLASS_PRICE_BYN": self.SINGLE_CLASS_PRICE_BYN,
            "SINGLE_CLASS_PRICE_EUR": self.SINGLE_CLASS_PRICE_EUR,
            "SUBSCRIPTION_4_CLASSES_PRICE_BYN": self.SUBSCRIPTION_4_BYN,
            "SUBSCRIPTION_4_CLASSES_PRICE_EUR": self.SUBSCRIPTION_4_EUR,
            "SUBSCRIPTION_8_CLASSES_PRICE_BYN": self.SUBSCRIPTION_8_BYN,
            "SUBSCRIPTION_8_CLASSES_PRICE_EUR": self.SUBSCRIPTION_8_EUR,
            "ONLINE_GROUP_PRICE_BYN": self.ONLINE_GROUP_PRICE_BYN,
            "ONLINE_GROUP_PRICE_EUR": self.ONLINE_GROUP_PRICE_EUR,
            "INDIVIDUAL_CLASS_PRICE_BYN": self.INDIVIDUAL_CLASS_PRICE_BYN,
            "INDIVIDUAL_CLASS_PRICE_EUR": self.INDIVIDUAL_CLASS_PRICE_EUR,

            # --- Links ---
            "COURSE_PAY_LINK": self.COURSE_PAY_LINK,
            "SITE": self.SITE,
            "TRIAL_MINI_COURSE": self.TRIAL_MINI_COURSE,
        }

    
    # --- TEXT SYSTEM ---

    def get_text(self, key: str, default: str = "", **kwargs):
        """
        Retrieve and format text.

        Supports:
        - \\n → real line breaks
        - {PRICE} → from Settings
        - {OTHER_TEXT} → nested texts
        - {name} → runtime variables
        """

        raw_text = self._texts.get(key, default)

        if not isinstance(raw_text, str):
            return default

        # Preserve line breaks
        text = raw_text.replace("\\n", "\n")

        try:
            # 1. Inject settings (prices, links)
            text = text.format(**self.to_dict())

            # 2. Inject nested texts
            text = text.format(**self._texts)

            # 3. Inject runtime variables
            text = text.format(**kwargs)

            return text

        except Exception as e:
            print(f"⚠️ Format error in '{key}': {e}")
            return text


    # --- LINKS ---

    @property
    def SITE(self):
        return self._get("SITE")

    @property
    def COURSE_PAY_LINK(self):
        return self._get("COURSE_PAY_LINK")

    @property
    def PAY_LINK(self):
        return self._get("PAY_LINK")

    @property
    def TRIAL_MINI_COURSE(self):
        return self._get("TRIAL_MINI_COURSE")


    # --- PRICES ---

    @property
    def ONLINE_GROUP_PRICE_BYN(self):
        return self._get_int("ONLINE_GROUP_PRICE_BYN")

    @property
    def ONLINE_GROUP_PRICE_EUR(self):
        return self._get_int("ONLINE_GROUP_PRICE_EUR")

    @property
    def COURSE_PRICE_BYN(self):
        return self._get_int("COURSE_PRICE_BYN")

    @property
    def COURSE_PRICE_EUR(self):
        return self._get_int("COURSE_PRICE_EUR")

    @property
    def SINGLE_CLASS_PRICE_BYN(self):
        return self._get_int("SINGLE_CLASS_PRICE_BYN")

    @property
    def SINGLE_CLASS_PRICE_EUR(self):
        return self._get_int("SINGLE_CLASS_PRICE_EUR")

    @property
    def INDIVIDUAL_CLASS_PRICE_BYN(self):
        return self._get_int("INDIVIDUAL_CLASS_PRICE_BYN")

    @property
    def INDIVIDUAL_CLASS_PRICE_EUR(self):
        return self._get_int("INDIVIDUAL_CLASS_PRICE_EUR")

    @property
    def SUBSCRIPTION_4_BYN(self):
        return self._get_int("SUBSCRIPTION_4_CLASSES_PRICE_BYN")

    @property
    def SUBSCRIPTION_4_EUR(self):
        return self._get_int("SUBSCRIPTION_4_CLASSES_PRICE_EUR")

    @property
    def SUBSCRIPTION_8_BYN(self):
        return self._get_int("SUBSCRIPTION_8_CLASSES_PRICE_BYN")

    @property
    def SUBSCRIPTION_8_EUR(self):
        return self._get_int("SUBSCRIPTION_8_CLASSES_PRICE_EUR")

    # --- OTHER SETTINGS ---

    @property
    def FOLLOWUP_CHECK_INTERVAL(self):
        return self._get_int("FOLLOWUP_CHECK_INTERVAL", 600)
 
# --- GLOBAL INSTANCE ---

settings = SettingsManager()


# --- BACKGROUND WORKER ---

async def config_updater_worker(interval=600):
    """
    Periodically refresh settings and texts from Grist.
    Runs without restarting the bot.
    """
    while True:
        await asyncio.sleep(interval)

        loop = asyncio.get_event_loop()
        success = await loop.run_in_executor(None, settings.refresh)

        if success:
            print("🔄 Config updated from Grist")