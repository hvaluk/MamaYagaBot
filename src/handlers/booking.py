# src/handlers/booking.py

from src.bot import bot
from src.keyboards.inline_kb import course_options_kb
from telebot.types import CallbackQuery
from src.services.requests import create_request

@bot.callback_query_handler(lambda c: c.data.startswith('fmt_'))
async def format_handler(call: CallbackQuery):
    format_chosen = call.data.split('_')[1]
    await create_request(call.from_user.id, request_type='course', format_chosen=format_chosen)
    kb = course_options_kb()
    await bot.send_message(call.message.chat.id, "Отлично! Выбери опцию:", reply_markup=kb)
