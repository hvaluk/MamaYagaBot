# src/handlers/welcome.py

from telebot.types import Message
from src.common import bot
from src.keyboards.inline_kb import build_inline_kb
from src.utils.grist_helper import get_grist_user, create_user
from src.utils.state_manager import set_state
from src.config import settings


@bot.message_handler(commands=["start", "help"])
async def send_welcome(message: Message):

    user_id = message.from_user.id
    chat_id = message.chat.id

    print(f"🚀 /start from {user_id}")

    # ---------- USER ----------
    user = await get_grist_user(user_id)

    if not user:
        print("👤 Creating new user")
        user = await create_user(message.from_user)

        text = settings.get_text(
            "WELCOME",
            name=message.from_user.first_name or ""
        )
    else:
        print("👤 Returning user")

        text = settings.get_text(
            "RETURNING_WELCOME",
            name=message.from_user.first_name or ""
        )

    # ---------- RESET STATE ----------
    await set_state(user_id, "idle")

    # ---------- UI ----------
    kb = await build_inline_kb("main_kb")

    await bot.send_message(
        chat_id,
        text,
        reply_markup=kb
    )