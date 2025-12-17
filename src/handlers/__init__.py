# from src.handlers.welcome import send_welcome
# from src.handlers.course_flow import  *
# from src.handlers.message import echo_message


# __all__ = ["echo_message",  "send_welcome"]

# src/handlers/__init__.py
# import handlers to register decorators on bot
 
from telebot.types import Message
from src.common import bot
from src.dao.models import AsyncSessionLocal, User, Request
from src.states import UserState
from src.config import OWNER_IDS


@bot.message_handler(content_types=["text"])
async def receive_contact(message: Message):
    async with AsyncSessionLocal() as session:
        user = await session.get(User, message.from_user.id)
        if not user or user.state != UserState.WAITING_CONTACT:
            return

        user.contact = message.text
        user.state = UserState.IDLE

        session.add_all([
            user,
            Request(
                user_id=user.telegram_id,
                request_type="contact",
                payload=message.text
            )
        ])
        await session.commit()

    for owner in OWNER_IDS:
        await bot.send_message(
            owner,
            f"📩 Новый контакт\n"
            f"@{user.username}\n"
            f"{message.text}"
        )

    await bot.send_message(
        message.chat.id,
        "Спасибо! 💛 Анна скоро напишет тебе."
    )
