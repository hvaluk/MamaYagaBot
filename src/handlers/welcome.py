from src.common import bot
from src.dao.models import User, AsyncSessionLocal
from telebot.async_telebot import types


@bot.message_handler(commands=['start', 'help'])
async def send_welcome(message):
    username = message.from_user.username
    first_name = message.from_user.first_name

    # имя для обращения
    display_name = first_name or (f"@{username}" if username else "друг")

    async with AsyncSessionLocal() as session:
        user = await session.get(User, message.from_user.id)

        if not user:
            # создаём пользователя
            user = User(
                telegram_id=message.from_user.id,
                username=username,
                first_name=first_name,
                last_name=message.from_user.last_name,
            )
            session.add(user)
            await session.commit()

            # Первое личное приветствие
            await bot.send_message(
                message.chat.id,
                f"Привет, {display_name}! 🌿\nРада знакомству 🤗"
            )
        else:
            # Приветствие для вернувшихся
            await bot.send_message(
                message.chat.id,
                f"С возвращением, {display_name}! 🌿"
            )

    # Основной экран
    text = (
        "Я бот-помощник Анны.\n"
        "Помогу тебе узнать о йоге для беременных "
        "и практиках женского здоровья.\n\n"
        "С чего начнём?"
    )

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Йога для беременных")
    btn2 = types.KeyboardButton("Советы и вдохновение")
    btn3 = types.KeyboardButton("Записаться")

    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)

    await bot.send_message(message.chat.id, text, reply_markup=markup)
