# src/handlers/flow_pregnancy.py

from src.bot import bot
from src.keyboards.inline_kb import pregnancy_kb
from telebot.types import CallbackQuery

@bot.callback_query_handler(lambda c: c.data == 'start_course_flow' or c.data == 'menu_trial')
async def start_course_flow(call: CallbackQuery):
    await bot.send_message(
        call.message.chat.id,
        "Отлично! Подберу для тебя безопасный и подходящий формат занятий 🙏\n"
        "Подскажи, какой у тебя срок беременности?"
    )
    kb = pregnancy_kb()
    await bot.send_message(call.message.chat.id, "Выбери срок:", reply_markup=kb)
