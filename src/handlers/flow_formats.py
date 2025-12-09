# src/handlers/flow_formats.py

from src.bot import bot
from src.keyboards.inline_kb import formats_kb
from telebot.types import CallbackQuery

@bot.callback_query_handler(lambda c: c.data.startswith('contra_'))
async def contra_handler(call: CallbackQuery):
    user_choice = call.data
    if user_choice in ['contra_yes', 'contra_unsure']:
        text = (
            "При противопоказаниях к активному образу жизни во время беременности, "
            "в йоге есть особенные бережные практики, которые могут подойти тебе. "
            "Узнаем подробнее через личную переписку."
        )
        await bot.send_message(call.message.chat.id, text)
    kb = formats_kb()
    await bot.send_message(call.message.chat.id, "Теперь выбери удобный формат занятий:", reply_markup=kb)
