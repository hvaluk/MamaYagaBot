# src/keyboards/inline_kb.py

from telebot import types
from src.utils.grist_helper import get_buttons_for_keyboard

async def build_inline_kb(name: str, **kwargs) -> types.InlineKeyboardMarkup:
    """
    Build inline keyboard from Grist with dynamic variables (e.g. app_id)
    """
    kb = types.InlineKeyboardMarkup()
    buttons = await get_buttons_for_keyboard(name)
    buttons.sort(key=lambda b: b["row_order"])

    row_dict = {}
    for btn in buttons:
        callback_data = btn["callback_data"]
        # 🔥 Safe injection of dynamic variables
        try:
            callback_data = callback_data.format(**kwargs)
        except KeyError:
            pass

        inline_btn = types.InlineKeyboardButton(
            text=btn["label"],
            callback_data=callback_data,
            request_contact=btn.get("request_contact", False)
        )

        # Group buttons by row_order
        row_order = btn.get("row_order", 0)
        if row_order not in row_dict:
            row_dict[row_order] = []
        row_dict[row_order].append(inline_btn)

    # Add all rows to keyboard
    for row in sorted(row_dict.keys()):
        kb.row(*row_dict[row])

    return kb