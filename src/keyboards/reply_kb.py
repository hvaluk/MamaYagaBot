# src/keyboards/reply_kb.py
from telebot import types

def contact_request_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(types.KeyboardButton("Отправить номер телефона", request_contact=True))
    kb.add(types.KeyboardButton("Назад"))
    return kb
