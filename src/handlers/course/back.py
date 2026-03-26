# src/handlers/course/back.py

from src.common import bot
from src.config import settings
from src.keyboards.inline_kb import build_inline_kb
from src.keyboards.reply_kb import build_reply_kb
from src.utils.state_manager import get_state, get_context, set_state

async def handle_back(user_id: int, chat_id: int):
    """
    Handles 'back' button for contact flow and other steps.
    """
    state = await get_state(user_id)
    ctx = await get_context(user_id)
    flow = ctx.get("flow")
    fmt = ctx.get("format")

    # -------- CONTACT FLOW --------
    if state == "course_contact":
        # go back to previous step (e.g., request selection or main kb)
        kb = await build_inline_kb("consult_offer_kb")  # or another previous kb
        await set_state(user_id, "course_offer")
        await bot.send_message(chat_id, settings.get_text("FREE_CONSULT_OFFER"), reply_markup=kb)
        return

    # -------- OTHER FLOWS --------
    kb = await build_inline_kb("main_kb")
    await set_state(user_id, "idle")
    await bot.send_message(chat_id, settings.get_text("HELP_TEXT"), reply_markup=kb)