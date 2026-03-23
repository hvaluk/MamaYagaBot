# src/handlers/course/back.py
"""
Handler for "back" button/navigation using GRIST for state/context.
"""

from src.common import bot
from src.config import settings
from src.keyboards.inline_kb import formats_kb, main_kb
from src.utils.state_manager import get_state, get_context, set_state

async def handle_back(user_id: int, chat_id: int):
    """
    Handles 'back' action based on current GRIST application state and context.
    """
    state = await get_state(user_id)
    ctx = await get_context(user_id)

    flow = ctx.get("flow")
    fmt = ctx.get("format")

    # -------- TRIAL / COURSE INFO --------
    if flow in {"trial", "course_info"}:
        await set_state(user_id, "idle")
        await bot.send_message(chat_id, settings.get_text("HELP_TEXT"), reply_markup=main_kb())
        return

    # -------- CONTRAINDICATION FLOW --------
    if fmt == "contra":
        await set_state(user_id, "idle")
        await bot.send_message(chat_id, settings.get_text("HELP_TEXT"), reply_markup=main_kb())
        return

    # -------- CONTACT FLOW --------
    if state == "course_contact":
        await set_state(user_id, "course_format")
        await bot.send_message(chat_id, settings.get_text("FORMAT_TEXT"), reply_markup=formats_kb())
        return

    # -------- PAY / FORMAT FLOW --------
    if state in {"course_pay", "course_format"}:
        await set_state(user_id, "course_format")
        await bot.send_message(chat_id, settings.get_text("FORMAT_TEXT"), reply_markup=formats_kb())
        return

    # -------- FALLBACK --------
    await set_state(user_id, "idle")
    await bot.send_message(chat_id, settings.get_text("HELP_TEXT"), reply_markup=main_kb())