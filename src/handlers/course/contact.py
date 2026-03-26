# src/handlers/course/contact.py

import re
import json
from datetime import datetime, timezone
from telebot.types import Message, Contact, ReplyKeyboardRemove

from src.common import bot
from src.config import OWNER_IDS
from src.utils.state_manager import get_state, set_state, get_application, update_application
from src.handlers.course.back import handle_back
from src.utils.humanize import humanize, TERM_MAP, EXP_MAP, CONTRA_MAP, FORMAT_MAP

FORBIDDEN_CONTACT_VALUES = {"назад", "back", "/start", "старт"}

# --- HELPER ---
def format_human_datetime(value) -> str:
    """Convert ISO/timestamp to human-readable UTC string"""
    if isinstance(value, (int, float)):
        dt = datetime.fromtimestamp(value, tz=timezone.utc)
    elif isinstance(value, str):
        try:
            dt = datetime.fromisoformat(value)
        except Exception:
            dt = datetime.now(timezone.utc)
    else:
        dt = datetime.now(timezone.utc)
    return dt.strftime("%d.%m.%Y %H:%M UTC")

def is_valid_phone(text: str) -> bool:
    return bool(re.fullmatch(r"^\+?\d{7,15}$", text))

def is_valid_username(text: str) -> bool:
    return bool(re.fullmatch(r"^@[\w\d_]{5,32}$", text))


# --- HANDLER ---
@bot.message_handler(content_types=["text", "contact"])
async def receive_contact(message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    # --- STATE CHECK ---
    state = await get_state(user_id)
    if state != "course_contact":
        return

    # --- BACK BUTTON ---
    if message.text and message.text.lower() in {"назад", "back"}:
        await handle_back(user_id, chat_id)
        return

    # --- EXTRACT CONTACT ---
    contact: str | None = None
    if message.contact and isinstance(message.contact, Contact):
        contact = message.contact.phone_number
    elif message.text:
        contact = message.text.strip()

    if not contact or contact.lower() in FORBIDDEN_CONTACT_VALUES:
        await bot.send_message(chat_id, "Пожалуйста, отправь корректный номер телефона или Telegram @username")
        return

    if not (is_valid_phone(contact) or is_valid_username(contact)):
        await bot.send_message(chat_id, "Неверный формат номера или @username, попробуй снова")
        return

    # --- GET APPLICATION ---
    app = await get_application(user_id)
    if not app:
        await bot.send_message(chat_id, "Ошибка. Попробуй начать заново 🙏")
        await set_state(user_id, "idle")
        return

    # --- UPDATE APPLICATION ---
    await update_application(user_id, {
        "contact": contact,
        "current_step": "contact_submitted",
        "status": "submitted"
    })
    await set_state(user_id, "idle")

    # --- CONFIRM TO USER ---
    await bot.send_message(
        chat_id,
        "Спасибо! 💛\nАнна свяжется с тобой в ближайшее время.",
        reply_markup=ReplyKeyboardRemove()
    )

    # --- SEND TO ADMINS ---
    fields = app.get("fields", {})
    try:
        feelings = json.loads(fields.get("feelings") or "[]")
    except Exception:
        feelings = []

    text = (
        f"Заявка #{app['id']}\n\n"
        f"Пользователь: {message.from_user.first_name or ''} {message.from_user.last_name or ''}\n"
        f"Username: @{message.from_user.username or '—'}\n"
        f"Telegram ID: {user_id}\n\n"
        f"Срок: {fields.get('pregnancy_term', '—')}\n"
        f"Чувства: {', '.join(feelings) if feelings else '—'}\n"
        f"Опыт: {fields.get('yoga_experience', '—')}\n"
        f"Запрос: {fields.get('request_type', '—')}\n"
        f"Формат: {fields.get('format', '—')}\n"
        f"Контакт: {contact}\n"
        f"Дата создания: {format_human_datetime(fields.get('created_at'))}"
    )

    for owner_id in OWNER_IDS:
        try:
            await bot.send_message(owner_id, text)
        except Exception as e:
            print(f"Failed to notify owner {owner_id}: {e}")