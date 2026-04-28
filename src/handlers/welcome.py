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

    user_record = await get_grist_user(user_id)

    if not user_record:
        print("👤 Creating new user")
        user_record = await create_user(message.from_user)

        name = message.from_user.first_name or ""
        text = settings.get_text("WELCOME", name=name)

    else:
        print("👤 Returning user")

        fields = user_record.get("fields", {})

        name = fields.get("FirstName") or ""
        text = settings.get_text("RETURNING_WELCOME", name=name)

    await set_state(user_id, "idle")

    kb = await build_inline_kb("main_kb")

    await bot.send_message(
        chat_id,
        text,
        reply_markup=kb
    )