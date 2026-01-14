# src/handlers/course/contact.py

from telebot.types import Message
from src.common import bot 
from src.config import OWNER_IDS
from src.dao.models import AsyncSessionLocal, User, Request
from src.states import get_state, clear_state, UserState



@bot.message_handler(func=lambda m: get_state(m.from_user.id) == UserState.WAITING_CONTACT)
async def save_contact(message: Message):
    """
    Сохраняет контакт пользователя и уведомляет владельцев бота.
    """
    user_id = message.from_user.id
    chat_id = message.chat.id
    contact_text = message.text.strip()

    # Сохраняем в базу
    async with AsyncSessionLocal() as session:
        user = await session.get(User, user_id)
        if not user:
            return

        session.add(
            Request(
                user_id=user.telegram_id,
                request_type="contact_info",
                payload=contact_text
            )
        )
        await session.commit()

    # Отправляем владельцам уведомление
    for owner_id in OWNER_IDS:
        await bot.send_message(
            owner_id,
            f"📩 Новый контакт от @{message.from_user.username or message.from_user.id}:\n"
            f"{contact_text}"
        )

    # Подтверждение пользователю
    await bot.send_message(chat_id, "Спасибо! Мы свяжемся с тобой в ближайшее время 💛")

    # Очищаем состояние
    clear_state(user_id)
