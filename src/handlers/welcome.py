# src/handlers/welcome.py

from telebot.types import Message
from src.common import bot
from src.dao.models import AsyncSessionLocal, User
from src.keyboards.inline_kb import main_kb
from src.texts.start import WELCOME, RETURNING_WELCOME
from src.states import set_state, UserState

@bot.message_handler(commands=["start", "help"])
async def send_welcome(message: Message):
    async with AsyncSessionLocal() as session:
        user = await session.get(User, message.from_user.id)

        if not user:
            user = User(
                telegram_id=message.from_user.id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
            )
            session.add(user)
            text = WELCOME
        else:
            text = RETURNING_WELCOME

        await session.commit()

    await bot.send_message(message.chat.id, text, reply_markup=main_kb())
    set_state(message.from_user.id, UserState.IDLE)
