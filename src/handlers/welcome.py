# src/handlers/welcome.py

from telebot.types import Message
from src.common import bot
from src.keyboards.reply_kb import build_inline_kb
from src.utils.grist_helper import get_grist_user, create_user
from src.config import settings

@bot.message_handler(commands=["start", "help"])
async def send_welcome(message: Message):
    user_id = message.from_user.id

    existing_user = await get_grist_user(user_id)

    # NEW USER
    if not existing_user:
        await create_user(message.from_user)
        text = settings.get_text(
            "WELCOME",
            name=message.from_user.first_name or ""
        )
    # RETURNING USER
    else:
        text = settings.get_text(
            "RETURNING_WELCOME",
            name=message.from_user.first_name or ""
        )

    # SEND MAIN KEYBOARD
    kb = await build_inline_kb("main_kb")
    await bot.send_message(message.chat.id, text, reply_markup=kb)