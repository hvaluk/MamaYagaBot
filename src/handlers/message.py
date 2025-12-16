# src/handlers/message.py

# from src.common import bot

# @bot.message_handler(func=lambda m: m.text and not m.text.startswith('/'))
# async def echo_message(message):
#     await bot.send_message(message.chat.id, "Спасибо! Чтобы выбрать действие — нажми /start")

from telebot.types import Message
from src.common import bot
from src.dao.models import AsyncSessionLocal, User, Request
from src.states import UserState
from src.config import OWNER_IDS


from telebot.types import Message
from src.common import bot
from src.dao.models import AsyncSessionLocal, User, Request
from src.states import UserState
from src.config import OWNER_IDS

@bot.message_handler(content_types=["text"])
async def receive_contact(message: Message):
    """Обработка контакта пользователя при противопоказаниях"""
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
