# src/keyboards/reply_kb.py

from telebot import types
from src.utils.grist_helper import get_buttons_for_keyboard

async def build_reply_kb(name: str) -> types.ReplyKeyboardMarkup:
    """
    Build reply keyboard from Grist 'Buttons' table
    """
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = await get_buttons_for_keyboard(name)
    buttons.sort(key=lambda b: b["row_order"])

    for btn in buttons:
        kb.add(types.KeyboardButton(
            text=btn["label"],
            request_contact=btn.get("request_contact", False)
        ))

    return kb


async def build_inline_kb(name: str) -> types.InlineKeyboardMarkup:
    """
    Build inline keyboard from Grist 'Buttons' table
    """
    kb = types.InlineKeyboardMarkup()
    buttons = await get_buttons_for_keyboard(name)
    buttons.sort(key=lambda b: b["row_order"])

    for btn in buttons:
        kb.add(types.InlineKeyboardButton(
            text=btn["label"],
            callback_data=btn.get("callback_data", btn["label"])
        ))
    return kb