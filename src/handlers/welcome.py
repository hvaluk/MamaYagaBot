# src/handlers/welcome.py

from src.common import bot
from src.dao.models import AsyncSessionLocal, User
from src.keyboards.inline_kb import main_kb
from telebot.types import Message
from src.texts.start import WELCOME, RETURNING_WELCOME

@bot.message_handler(commands=['start', 'help'])
async def send_welcome(message: Message):
    async with AsyncSessionLocal() as session:
        async with session.begin():  # открываем транзакцию
            # Проверяем, есть ли пользователь
            user = await session.get(User, message.from_user.id)
            if not user:
                user = User(
                    telegram_id=message.from_user.id,
                    username=message.from_user.username,
                    first_name=message.from_user.first_name,
                    last_name=message.from_user.last_name
                )
                session.add(user)  # добавляем нового пользователя
                text = WELCOME
            else:
                text = RETURNING_WELCOME

        # commit автоматически выполняется при выходе из async with session.begin()

    await bot.send_message(
        message.chat.id,
        text,
        reply_markup=main_kb()
    )
