from src.common import bot
from src.dao.models import User, AsyncSessionLocal


@bot.message_handler(commands=['start', 'help'])
async def send_welcome(message):
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
            await session.commit()
            await bot.reply_to(message, "Добро пожаловать! Вы зарегистрированы.")
        else:
            await bot.reply_to(message, "C возвращением!")

    text = 'Привет, я бот-помощник Анны. \nЯ помогу тебе узнать о йоге для беременных.'
    await bot.reply_to(message, text)