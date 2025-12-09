# src/handlers/flow_contra.py

from src.bot import bot
from src.keyboards.inline_kb import experience_kb
from telebot.types import CallbackQuery

@bot.callback_query_handler(lambda c: c.data.startswith('term_'))
async def pregnancy_term(call: CallbackQuery):
    await bot.send_message(call.message.chat.id, "Здорово! Еще один уточняющий вопрос: ты раньше пробовала заниматься йогой?")
    kb = experience_kb()
    await bot.send_message(call.message.chat.id, "Выбери вариант:", reply_markup=kb)
