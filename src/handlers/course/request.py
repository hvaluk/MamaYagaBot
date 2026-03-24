# src/handlers/course/request.py

import asyncio
from telebot.types import CallbackQuery
from src.common import bot
from src.keyboards.inline_kb import build_inline_kb
from src.config import settings
from src.utils.state_manager import get_state, set_state, update_application, get_application
from src.utils.humanize import REQUEST_MAP

@bot.callback_query_handler(func=lambda c: c.data in REQUEST_MAP)
async def course_request(call: CallbackQuery):
    """
    Handler for user's main request selection (ASK_REQUEST + request_kb)
    1️⃣ Saves selection in Grist
    2️⃣ Sends empathetic response (SAFE_TEXT)
    3️⃣ After short delay, sends FREE_CONSULT_OFFER with consult_offer_kb
    """
    user_id = call.from_user.id
    chat_id = call.message.chat.id

    # --- STATE CHECK ---
    state = await get_state(user_id)
    if state != "course_request":
        return

    # --- acknowledge callback ---
    await bot.answer_callback_query(call.id)

    # --- map callback to human-readable value ---
    value = REQUEST_MAP[call.data]

    # --- get user's application from Grist ---
    app = await get_application(user_id)
    if not app:
        await bot.send_message(chat_id, "Error: please restart the process.")
        await set_state(user_id, "idle")
        return

    # --- save request_type in Grist ---
    await update_application(user_id, {"request_type": value})

    # --- move user to next internal state ---
    await set_state(user_id, "course_offer")

    # --- 1️⃣ Send empathetic response ---
    safe_text = settings.get_text("SAFE_TEXT")
    await bot.send_message(chat_id, safe_text)

    # --- 2️⃣ short delay for better UX ---
    await asyncio.sleep(3)  

    # --- 3️⃣ Send consultation offer with inline buttons ---
    offer_text = settings.get_text("CONSULT_OFFER_TEXT")
    kb = await build_inline_kb("consult_offer_kb")
    await bot.send_message(chat_id, offer_text, reply_markup=kb)