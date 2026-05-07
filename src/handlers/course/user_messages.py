# src/handlers/course/user_messages.py

print("✅ user_messages handler registered")

from telebot.types import Message
from datetime import datetime, timezone

from src.common import bot
from src.utils.state_manager import (
    get_state,
    set_state,
    get_application,
    update_application
)
from src.utils.grist_helper import get_grist_user, create_user_message
from src.config import ADMIN_IDS


# -------------------- ADMIN NOTIFY --------------------
async def notify_admins(text: str):
    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(admin_id, text)
        except Exception as e:
            print(f"❌ ADMIN SEND ERROR [{admin_id}]: {e}")


def format_msg(user, text: str):
    return (
        f"💬 НОВОЕ СООБЩЕНИЕ\n\n"
        f"{user.first_name or ''} {user.last_name or ''}\n"
        f"@{user.username or '—'}\n"
        f"ID: {user.id}\n\n"
        f"{text}"
    )


# -------------------- HANDLER --------------------
@bot.message_handler(func=lambda m: True, content_types=["text"])
async def handle_user_messages(message: Message):

    user_id = message.from_user.id
    chat_id = message.chat.id
    text = (message.text or "").strip()

    print(f"🔥 MESSAGE CAPTURED [{user_id}]: {text}")

    # --- IGNORE SYSTEM ---
    if not text or text.startswith("/"):
        return

    # --- STATE CHECK ---
    state = await get_state(user_id)
    if state != "course_message":
        return

    # --- GET USER ---
    user = await get_grist_user(user_id)
    if not user:
        print(f"❌ USER NOT FOUND: {user_id}")
        return

    # --- GET APPLICATION ---
    app = await get_application(user_id)

    # --- SAVE MESSAGE ---
    try:
        create_user_message(
            user_row_id=user["id"],
            application_id=app["id"] if app else None,
            message_text=text,
            state=state
        )
        print("✅ MESSAGE SAVED")

    except Exception as e:
        print("❌ SAVE MESSAGE ERROR:", e)
        return

    # --- STOP FOLLOWUP (user engaged) ---
    if app:
        try:
            await update_application(user_id, {
                "followup_stage": 99,  # Полная остановка
                "status": "message_received"
            })
            print(f"✅ Follow-up stopped for {user_id} (message received)")
        except Exception as e:
            print("❌ FOLLOWUP STOP ERROR:", e)


    # --- ADMIN NOTIFY ---
    try:
        await notify_admins(format_msg(message.from_user, text))
    except Exception as e:
        print("❌ ADMIN NOTIFY ERROR:", e)

    # --- USER RESPONSE ---
    try:
        await bot.send_message(
            chat_id,
            "💛 Спасибо! Я передала сообщение Анне."
        )
    except Exception as e:
        print("❌ USER RESPONSE ERROR:", e)

    # --- RESET STATE ---
    await set_state(user_id, "idle")