# src/handlers/menu.py

from telebot import types
from src.common import bot
from src.config import PAY_LINK, TRIAL_VIDEO, TRIAL_LECT, SITE

@bot.callback_query_handler(func=lambda c: c.data == "menu_book")
async def cb_menu_book(call):
    await bot.answer_callback_query(call.id)
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Йога для беременных онлайн", callback_data="book_online"))
    kb.add(types.InlineKeyboardButton("Индивидуальное занятие", callback_data="book_individual"))
    kb.add(types.InlineKeyboardButton("Консультация", callback_data="book_consult"))
    kb.add(types.InlineKeyboardButton("Назад", callback_data="menu_back"))
    await bot.send_message(call.message.chat.id, "Выберите формат занятия:", reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data == "menu_trial")
async def cb_menu_trial(call):
    await bot.answer_callback_query(call.id)
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Пробный урок (видео)", url=TRIAL_VIDEO))
    kb.add(types.InlineKeyboardButton("Первая лекция", url=TRIAL_LECT))
    kb.add(types.InlineKeyboardButton("Назад", callback_data="menu_back"))
    await bot.send_message(call.message.chat.id, "Пробные материалы:", reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data == "menu_back")
async def cb_menu_back(call):
    await bot.answer_callback_query(call.id)
    await bot.send_message(call.message.chat.id, "Возвращаю в главное меню. Нажми /start")

