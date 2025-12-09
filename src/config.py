# src/config.py

# from dotenv import load_dotenv
# import os

# # Load environment variables from .env
# load_dotenv()


# # Telegram

# TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
# ADMIN_IDS = [int(x) for x in os.getenv('ADMIN_IDS', '').split(',') if x.strip()]

# # Airtable

# AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')
# AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')
# USERS_TABLE = os.getenv('AIRTABLE_USERS_TABLE', 'Users')
# REQUESTS_TABLE = os.getenv('AIRTABLE_REQUESTS_TABLE', 'Requests')


# # Links and texts

# SITE = os.getenv('SITE', 'https://example.com')
# TRIAL_VIDEO = os.getenv('TRIAL_VIDEO', '')
# TRIAL_LECT = os.getenv('TRIAL_LECT', '')
# COURSE_PAY_LINK = os.getenv('COURSE_PAY_LINK', '')

# # Prices (BYN and EUR)

# def parse_int_env(name: str, default: int) -> int:
#     try:
#         return int(os.getenv(name, default))
#     except ValueError:
#         return default

# COURSE_PRICE_BYN = parse_int_env('COURSE_PRICE_BYN', 190)
# COURSE_PRICE_EUR = parse_int_env('COURSE_PRICE_EUR', 55)

# SINGLE_CLASS_PRICE_BYN = parse_int_env('SINGLE_CLASS_PRICE_BYN', 40)
# SINGLE_CLASS_PRICE_EUR = parse_int_env('SINGLE_CLASS_PRICE_EUR', 12)

# SUBSCRIPTION_4_CLASSES_PRICE_BYN = parse_int_env('SUBSCRIPTION_4_CLASSES_PRICE_BYN', 150)
# SUBSCRIPTION_4_CLASSES_PRICE_EUR = parse_int_env('SUBSCRIPTION_4_CLASSES_PRICE_EUR', 48)

# SUBSCRIPTION_8_CLASSES_PRICE_BYN = parse_int_env('SUBSCRIPTION_8_CLASSES_PRICE_BYN', 300)
# SUBSCRIPTION_8_CLASSES_PRICE_EUR = parse_int_env('SUBSCRIPTION_8_CLASSES_PRICE_EUR', 90)

# # Form currency strings for display to the user

# COURSE_PRICE = f"{COURSE_PRICE_BYN} BYN / {COURSE_PRICE_EUR}€"
# SINGLE_CLASS_PRICE = f"{SINGLE_CLASS_PRICE_BYN} BYN / {SINGLE_CLASS_PRICE_EUR}€"
# SUBSCRIPTION_4_CLASSES_PRICE = f"{SUBSCRIPTION_4_CLASSES_PRICE_BYN} BYN / {SUBSCRIPTION_4_CLASSES_PRICE_EUR}€"
# SUBSCRIPTION_8_CLASSES_PRICE = f"{SUBSCRIPTION_8_CLASSES_PRICE_BYN} BYN / {SUBSCRIPTION_8_CLASSES_PRICE_EUR}€"

# # Worker

# FOLLOWUP_CHECK_INTERVAL = parse_int_env('FOLLOWUP_CHECK_INTERVAL', 3600)  # in seconds  

from dotenv import load_dotenv
import os

load_dotenv()

# Telegram
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
ADMIN_IDS = [int(x) for x in os.getenv('ADMIN_IDS', '').split(',') if x.strip()]

# Airtable
AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')
AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')
USERS_TABLE = os.getenv('AIRTABLE_USERS_TABLE', 'Users')
REQUESTS_TABLE = os.getenv('AIRTABLE_REQUESTS_TABLE', 'Requests')

# Links
SITE = os.getenv('SITE')
TRIAL_VIDEO = os.getenv('TRIAL_VIDEO')
TRIAL_LECT = os.getenv('TRIAL_LECT')
COURSE_PAY_LINK = os.getenv('COURSE_PAY_LINK')

# Prices
COURSE_PRICE_BYN = int(os.getenv('COURSE_PRICE_BYN', '190'))
COURSE_PRICE_EUR = int(os.getenv('COURSE_PRICE_EUR', '55'))
SINGLE_CLASS_PRICE_BYN = int(os.getenv('SINGLE_CLASS_PRICE_BYN', '40'))
SINGLE_CLASS_PRICE_EUR = int(os.getenv('SINGLE_CLASS_PRICE_EUR', '12'))
SUBSCRIPTION_4_CLASSES_PRICE_BYN = int(os.getenv('SUBSCRIPTION_4_CLASSES_PRICE_BYN', '150'))
SUBSCRIPTION_4_CLASSES_PRICE_EUR = int(os.getenv('SUBSCRIPTION_4_CLASSES_PRICE_EUR', '48'))
SUBSCRIPTION_8_CLASSES_PRICE_BYN = int(os.getenv('SUBSCRIPTION_8_CLASSES_PRICE_BYN', '300'))
SUBSCRIPTION_8_CLASSES_PRICE_EUR = int(os.getenv('SUBSCRIPTION_8_CLASSES_PRICE_EUR', '90'))

# Formatted strings
COURSE_PRICE = f"{COURSE_PRICE_BYN} BYN / {COURSE_PRICE_EUR}€"
SINGLE_CLASS_PRICE = f"{SINGLE_CLASS_PRICE_BYN} BYN / {SINGLE_CLASS_PRICE_EUR}€"
SUBSCRIPTION_4_CLASSES_PRICE = f"{SUBSCRIPTION_4_CLASSES_PRICE_BYN} BYN / {SUBSCRIPTION_4_CLASSES_PRICE_EUR}€"
SUBSCRIPTION_8_CLASSES_PRICE = f"{SUBSCRIPTION_8_CLASSES_PRICE_BYN} BYN / {SUBSCRIPTION_8_CLASSES_PRICE_EUR}€"

# Follow-up
FOLLOWUP_CHECK_INTERVAL = int(os.getenv('FOLLOWUP_CHECK_INTERVAL', '3600'))
