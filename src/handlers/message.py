# src/handlers/message.py
from telebot.types import Message
from src.common import bot
from src.dao.models import AsyncSessionLocal, User, Request
from src.states import get_state, clear_state, UserState

@bot.message_handler(content_types=["text"])
async def receive_contact(message: Message):
    user_id = message.from_user.id
    state = get_state(user_id)
    if state != UserState.WAITING_CONTACT:
        return

    async with AsyncSessionLocal() as session:
        user = await session.get(User, user_id)
        if not user:
            return
        user.phone = message.text
        session.add(Request(
            user_id=user.telegram_id,
            request_type="contact",
            payload=message.text
        ))
        await session.commit()

    clear_state(user_id)
    await bot.send_message(message.chat.id, "Спасибо! 💛 Анна скоро напишет тебе.")
