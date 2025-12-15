# src/handlers/welcome.py

from email.mime import message, text
from src.common import bot
from src.dao.models import AsyncSessionLocal, User
from src.keyboards.inline_kb import main_kb

@bot.message_handler(commands=['start', 'help'])
async def send_welcome(message):
    # text = 'Привет!\nЯ помощник Анны. Помогу тебе хорошо чувствовать себя во время беременности и подготовиться к родам.\n\nС чего начнём?'
    # await bot.reply_to(message, text)   

    async with AsyncSessionLocal() as session:
        user = await session.get(User, message.from_user.id)
        if not user:
            user = User(
                telegram_id=message.from_user.id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name
            )
            session.add(user)
            await session.commit()
            text = ('Привет!\nЯ помощник Анны. Помогу тебе хорошо чувствовать себя во время беременности и подготовиться к родам.\n\nС чего начнём?')
        else:
            text = ('С возвращением!\nЯ помощник Анны. Помогу тебе хорошо чувствовать себя во время беременности и подготовиться к родам.\n\nС чего начнём?')

    await bot.send_message(
        message.chat.id, text,  
        reply_markup=main_kb()
    )