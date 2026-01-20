# src/keyboards/reply_kb.py

from telebot import types

def contact_request_kb():
    """Клавиатура для отправки контакта (номер телефона или Telegram)."""
    kb = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
    )
    kb.add(
        types.KeyboardButton(
            text="Отправить номер телефона",
            request_contact=True
        )
    )
    return kb
