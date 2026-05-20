# src/handlers/course/contact.py

import re
import json
from datetime import datetime
from telebot.types import Message, Contact, ReplyKeyboardRemove

from src.common import bot
from src.config import OWNER_IDS, MINSK_TZ
from src.utils.state_manager import (
    get_state,
    set_state,
    get_application,
    update_application
)
from src.utils.humanize import (
    humanize,
    FORMAT_MAP,
)


# ===================== VALIDATION =====================
FORBIDDEN_CONTACT_VALUES = {"назад", "back", "/start", "старт"}


def is_valid_phone(text: str) -> bool:
    return bool(re.fullmatch(r"^\+?\d{7,15}$", text))


def is_valid_username(text: str) -> bool:
    return bool(re.fullmatch(r"^@[\w\d_]{5,32}$", text))


def format_human_datetime(value) -> str:
    if isinstance(value, (int, float)):
        dt = datetime.fromtimestamp(value, tz=MINSK_TZ)
    elif isinstance(value, str):
        try:
            dt = datetime.fromisoformat(value).astimezone(MINSK_TZ)
        except Exception:
            dt = datetime.now(MINSK_TZ)
    else:
        dt = datetime.now(MINSK_TZ)

    return dt.strftime("%d.%m.%Y %H:%M +03:00")


# ===================== FILTER =====================
async def is_contact_state(message: Message) -> bool:
    state = await get_state(message.from_user.id)
    return state == "course_contact"


# ===================== CONTACT (BUTTON) =====================
@bot.message_handler(func=is_contact_state, content_types=["contact"])
async def receive_contact_button(message: Message):

    user_id = message.from_user.id
    chat_id = message.chat.id

    if not message.contact or not isinstance(message.contact, Contact):
        return

    contact = message.contact.phone_number

    await process_contact(user_id, chat_id, contact, message)


# ===================== CONTACT (TEXT) =====================
@bot.message_handler(func=is_contact_state, content_types=["text"])
async def receive_contact_text(message: Message):

    user_id = message.from_user.id
    chat_id = message.chat.id

    text = (message.text or "").strip()

    if not text:
        return

    if text.lower() in FORBIDDEN_CONTACT_VALUES:
        await bot.send_message(chat_id, "Пожалуйста, отправь номер телефона или @username")
        return

    if not (is_valid_phone(text) or is_valid_username(text)):
        await bot.send_message(
            chat_id,
            "Формат не распознан.\n\n"
            "Примеры:\n"
            "+4915712345678\n"
            "@username"
        )
        return

    await process_contact(user_id, chat_id, text, message)


# ===================== CORE LOGIC =====================
async def process_contact(user_id: int, chat_id: int, contact: str, message: Message):

    print(f"📞 CONTACT RECEIVED [{user_id}]: {contact}")

    # --- APPLICATION ---
    app = await get_application(user_id)
    if not app:
        await bot.send_message(chat_id, "Ошибка. Начни заново 🙏")
        await set_state(user_id, "idle")
        return

    # --- UPDATE ---
    try:
        await update_application(user_id, {
            "contact": contact,
            "status": "submitted",
            "current_step": "contact_submitted"
        })
        print("✅ Application updated")

    except Exception as e:
        print("❌ UPDATE APPLICATION ERROR:", e)
        await bot.send_message(chat_id, "Ошибка сохранения. Попробуй ещё раз 🙏")
        return

    # --- USER RESPONSE ---
    await bot.send_message(
        chat_id,
        "Спасибо! 💛\nАнна свяжется с тобой.",
        reply_markup=ReplyKeyboardRemove()
    )

    await set_state(user_id, "idle")

    # --- ADMIN NOTIFY ---
    await notify_admins(message, app, contact)


# ===================== ADMIN =====================
async def notify_admins(message: Message, app: dict, contact: str):

    fields = app.get("fields", {})

    try:
        feelings = json.loads(fields.get("feelings") or "[]")
    except Exception:
        feelings = []

    text = (
        f"Заявка #{app['id']}\n\n"
        f"Пользователь: {message.from_user.first_name or ''} {message.from_user.last_name or ''}\n"
        f"Username: @{message.from_user.username or '—'}\n"
        f"Telegram ID: {message.from_user.id}\n\n"
        f"Срок: {fields.get('pregnancy_term', '—')}\n"
        f"Чувства: {', '.join(feelings) if feelings else '—'}\n"
        f"Опыт: {fields.get('yoga_experience', '—')}\n"
        f"Запрос: {fields.get('request_type', '—')}\n"
        f"Формат: {humanize(fields.get('format'), FORMAT_MAP)}\n"
        f"Контакт: {contact}\n"
        f"Дата: {format_human_datetime(fields.get('created_at'))}"
    )

    for owner_id in OWNER_IDS:
        try:
            await bot.send_message(owner_id, text)
        except Exception as e:
            print(f"❌ ADMIN SEND ERROR [{owner_id}]: {e}")