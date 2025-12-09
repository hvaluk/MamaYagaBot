# src/handlers/flow_contra.py

from src.bot import bot
from src.keyboards.inline_kb import contra_kb
from telebot.types import CallbackQuery

@bot.callback_query_handler(lambda c: c.data.startswith('exp_'))
async def experience_handler(call: CallbackQuery):
    user_choice = call.data
    if user_choice in ['exp_none', 'exp_some']:
        text = (
            "Все практики, которые я готовлю для женщин во время беременности безопасны, "
            "даже если ты никогда не занималась йогой. Если у тебя нет медицинских противопоказаний "
            "и беременность протекает без серьезных осложнений — добро пожаловать на коврик 🧘‍♀️"
        )
    else:
        text = "Отлично! Переходим к следующему шагу."
    await bot.send_message(call.message.chat.id, text)
    kb = contra_kb()
    await bot.send_message(call.message.chat.id, "Есть ли у тебя противопоказания к занятиям?", reply_markup=kb)
