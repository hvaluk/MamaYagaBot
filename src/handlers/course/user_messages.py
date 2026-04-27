# src/handlers/course/user_messages.py

from telebot.types import Message

from src.common import bot
from src.utils.state_manager import get_state, set_state
from src.utils.grist_helper import get_grist_user, create_user_message
from src.config import ADMIN_IDS


# -------------------- ADMIN NOTIFY --------------------
async def notify_admins(text: str):
    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(admin_id, text)
        except Exception as e:
            print(f"❌ ADMIN SEND ERROR [{admin_id}]:", e)


def format_msg(user, text: str):
    return (
        f"💬 НОВОЕ СООБЩЕНИЕ\n\n"
        f"{user.first_name or ''} {user.last_name or ''}\n"
        f"@{user.username or '—'}\n"
        f"ID: {user.id}\n\n"
        f"{text}"
    )


# -------------------- HANDLER --------------------
@bot.message_handler(content_types=["text"])
async def handle_user_messages(message: Message):

    user_id = message.from_user.id
    text = (message.text or "").strip()

    if not text or text.startswith("/"):
        return

    state = await get_state(user_id)
    if state != "course_message":
        return

    user = await get_grist_user(user_id)
    if not user:
        return

    await create_user_message(
        user_row_id=user["id"],
        application_id=None,
        message_text=text,
        state=state
    )

    # ---------- ADMIN NOTIFY ----------
    try:
        await notify_admins(format_msg(message.from_user, text))
    except Exception as e:
        print("❌ ADMIN NOTIFY ERROR:", e)

    await bot.send_message(
        message.chat.id,
        "💛 Спасибо! Я передала сообщение Анне."
    )

    await set_state(user_id, "idle")