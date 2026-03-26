# src/handlers/course/user_messages.py

from telebot.types import Message
from src.common import bot
from src.config import OWNER_IDS
from src.utils.state_manager import get_state, get_application
from src.utils.grist_helper import get_grist_user, create_user_message


@bot.message_handler(func=lambda m: True, content_types=["text"])
async def user_message_handler(message: Message):
    user_id = message.from_user.id

    # ignore commands
    if message.text and message.text.startswith("/"):
        return

    text = message.text.strip() if message.text else ""

    state = await get_state(user_id)
    if not state:
        return

    app = await get_application(user_id)
    app_id = app["id"] if app else None

    try:
        grist_user = await get_grist_user(user_id)
        if grist_user:
            await create_user_message(
                user_id=grist_user["id"],
                application_id=app_id,
                message_text=text,
                state=state
            )
    except Exception as e:
        print(f"GRIST SAVE ERROR: {e}")

    forward_text = (
        f"📨 Message from user #{app_id or '—'}\n"
        f"{message.from_user.first_name or ''} {message.from_user.last_name or ''} "
        f"(@{message.from_user.username or '—'})\n"
        f"Step: {state}\n\n"
        f"{text}"
    )

    for owner_id in OWNER_IDS:
        try:
            await bot.send_message(owner_id, forward_text)
        except Exception as e:
            print(f"ADMIN SEND ERROR: {e}")