# src/handlers/welcome.py


# from telebot import types
# from src.common import bot
# from src.dao import crud
# from src.config import SITE

# @bot.message_handler(commands=["start", "help"])
# async def send_welcome(message):
#     tg = message.from_user
#     username = tg.username
#     first_name = tg.first_name or ""
#     display_name = first_name if first_name else (f"@{username}" if username else "друг")

#     user = await crud.get_user(tg.id)
#     if not user:
#         await crud.create_user(
#             user_id=tg.id,
#             username=username,
#             first_name=first_name,
#             last_name=tg.last_name,
#         )
#         await bot.send_message(message.chat.id, f"Привет, {display_name}! 🌿\nРада знакомству 🤗")
#     else:
#         await bot.send_message(message.chat.id, f"С возвращением, {display_name}! 🌿")

#     await crud.create_request(tg.id, "joined", None, None, followup_hours=24)

#     text = (
#         "Я — помощник Анны. Помогу тебе узнать о йоге для беременных и практиках женского здоровья.\n\n"
#         "С чего начнём?"
#     )
#     kb = types.InlineKeyboardMarkup()
#     kb.add(types.InlineKeyboardButton("✨ Хочу записаться", callback_data="menu_book"))
#     kb.add(types.InlineKeyboardButton("🧘 Хочу пробное занятие", callback_data="menu_trial"))
#     kb.add(types.InlineKeyboardButton("ℹ️ Хочу подробнее узнать", url=SITE))

#     await bot.send_message(message.chat.id, text, reply_markup=kb)

from src.common import bot
from src.dao.models import AsyncSessionLocal, User

@bot.message_handler(commands=['start', 'help'])
async def send_welcome(message):
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
            await bot.reply_to(message, 'Привет!\nЯ помощник Анны. Помогу тебе хорошо чувствовать себя во время беременности и подготовиться к родам.\n\nС чего начнём?')

        else:
            await bot.reply_to(message, 'С возвращением!\nЯ помощник Анны. Помогу тебе хорошо чувствовать себя во время беременности и подготовиться к родам.\n\nС чего начнём?')

   