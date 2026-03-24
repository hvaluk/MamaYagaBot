# src/handlers/course/contact.py

import re
import json
from telebot.types import Message, Contact, ReplyKeyboardRemove
from src.common import bot
from src.config import OWNER_IDS
from src.utils.state_manager import get_state, set_state, get_application, update_application

FORBIDDEN_CONTACT_VALUES = {"назад", "back", "/start", "старт"}


# --- VALIDATION HELPERS ---

def is_valid_phone(text: str) -> bool:
    """
    Validate phone number (simple international format)
    """
    return bool(re.fullmatch(r"^\+?\d{7,15}$", text))


def is_valid_username(text: str) -> bool:
    """
    Validate Telegram username
    """
    return bool(re.fullmatch(r"^@[a-zA-Z0-9_]{5,32}$", text))


# ---------------- HANDLER ----------------

@bot.message_handler(content_types=["text", "contact"])
async def receive_contact(message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    # --- STATE CHECK ---
    state = await get_state(user_id)
    if state != "course_contact":
        return

    # --- BACK ---
    if message.text and message.text.lower() == "назад":
        from src.handlers.course.back import handle_back
        await handle_back(user_id, chat_id)
        return

    # --- EXTRACT CONTACT ---
    contact: str | None = None

    if message.contact and isinstance(message.contact, Contact):
        contact = message.contact.phone_number

    elif message.text:
        contact = message.text.strip()

    # --- VALIDATION ---
    if (
        not contact
        or contact.lower() in FORBIDDEN_CONTACT_VALUES
        or not (is_valid_phone(contact) or is_valid_username(contact))
    ):
        await bot.send_message(
            chat_id,
            "Пожалуйста, отправь корректный номер телефона или Telegram @username"
        )
        return

    # --- GET APPLICATION ---
    app = await get_application(user_id)
    if not app:
        await bot.send_message(chat_id, "Ошибка. Попробуй начать заново")
        await set_state(user_id, "idle")
        return

    # --- UPDATE APPLICATION ---
    await update_application(user_id, {
        "contact": contact,
        "current_step": "done",
        "status": "done"
    })

    # --- CONFIRM TO USER ---
    await bot.send_message(
        chat_id,
        "Спасибо! Ваш контакт сохранён.",
        reply_markup=ReplyKeyboardRemove()
    )

    await set_state(user_id, "idle")

    # --- PREPARE DATA FOR ADMIN ---
    fields = app["fields"]

    try:
        feelings = json.loads(fields.get("feelings") or "[]")
    except:
        feelings = []

    # --- ADMIN MESSAGE ---
    text = (
        f"Заявка #{app['id']}\n"
        f"Пользователь: {message.from_user.first_name or ''} {message.from_user.last_name or ''}\n"
        f"Username: @{message.from_user.username or '—'}\n"
        f"Срок: {fields.get('pregnancy_term', '—')}\n"
        f"Чувства: {', '.join(feelings) if feelings else '—'}\n"
        f"Опыт: {fields.get('yoga_experience', '—')}\n"
        f"Противопоказания: {fields.get('contraindications', '—')}\n"
        f"Формат: {fields.get('format', '—')}\n"
        f"Контакт: {contact}\n"
        f"Дата создания: {fields.get('created_at', '')}"
    )

    # --- SEND TO ADMINS ---
    for owner_id in OWNER_IDS:
        try:
            await bot.send_message(owner_id, text)
        except Exception as e:
            print(f"Failed to notify owner {owner_id}: {e}")
