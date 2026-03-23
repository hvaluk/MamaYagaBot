# src/keyboards/inline_kb.py

from telebot import types
from src.utils.grist_helper import get_buttons_for_keyboard
import asyncio

async def build_inline_kb(name: str) -> types.InlineKeyboardMarkup:
    """
    Build inline keyboard from Grist 'Buttons' table
    """
    kb = types.InlineKeyboardMarkup()
    buttons = await get_buttons_for_keyboard(name)
    buttons.sort(key=lambda b: b["row_order"])

    row = []
    last_order = None
    for btn in buttons:
        inline_btn = types.InlineKeyboardButton(
            text=btn["label"],
            callback_data=btn["callback_data"]
        )
        if last_order is not None and btn["row_order"] != last_order:
            kb.row(*row)
            row = [inline_btn]
        else:
            row.append(inline_btn)
        last_order = btn["row_order"]

    if row:
        kb.row(*row)

    return kb