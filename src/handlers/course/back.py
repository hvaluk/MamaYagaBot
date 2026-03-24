# src/handlers/course/back.py
"""
Handler for "back" button/navigation using GRIST for state/context.
"""

from src.common import bot
from src.config import settings
from src.keyboards.inline_kb import build_inline_kb
from src.keyboards.reply_kb import build_reply_kb
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
        kb = await build_inline_kb("main_kb")
        await set_state(user_id, "idle")
        await bot.send_message(chat_id, settings.get_text("HELP_TEXT"), reply_markup=kb)
        return

    # -------- CONTRAINDICATION FLOW --------
    if fmt == "contra":
        kb = await build_reply_kb("contact_request_kb")
        await set_state(user_id, "idle")
        await bot.send_message(chat_id, settings.get_text("HELP_TEXT"), reply_markup=kb)
        return

    # -------- CONTACT FLOW --------
    if state == "course_contact":
        kb = await build_reply_kb("contact_request_kb")
        await set_state(user_id, "course_format")
        await bot.send_message(chat_id, settings.get_text("FORMAT_TEXT"), reply_markup=kb)
        return

    # -------- PAY / FORMAT FLOW --------
    if state in {"course_pay", "course_format"}:
        kb = await build_inline_kb("formats_kb")
        await set_state(user_id, "course_format")
        await bot.send_message(chat_id, settings.get_text("FORMAT_TEXT"), reply_markup=kb)
        return

    # -------- FALLBACK --------
    kb = await build_inline_kb("main_kb")
    await set_state(user_id, "idle")
    await bot.send_message(chat_id, settings.get_text("HELP_TEXT"), reply_markup=kb)