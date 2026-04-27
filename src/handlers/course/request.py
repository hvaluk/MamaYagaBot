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

    user_id = call.from_user.id
    chat_id = call.message.chat.id

    # --- STATE GUARD ---
    state = await get_state(user_id)
    if state != "course_request":
        await bot.answer_callback_query(call.id)
        return

    await bot.answer_callback_query(call.id)

    # --- SAFE MAP ---
    value = REQUEST_MAP.get(call.data)
    if not value:
        return

    # --- LOAD APP ---
    app = await get_application(user_id)
    if not app:
        await bot.send_message(chat_id, "Error: restart flow.")
        await set_state(user_id, "idle")
        return

    # --- SAVE DATA (ONLY DATA LAYER) ---
    await update_application(user_id, {
        "request_type": value
    })

    # --- UX STEP 1 ---
    await bot.send_message(
        chat_id,
        settings.get_text("SAFE_TEXT")
    )

    # --- UX STEP 2 ---
    await asyncio.sleep(2)

    # --- UX STEP 3 ---
    kb = await build_inline_kb("consult_offer_kb")

    await bot.send_message(
        chat_id,
        settings.get_text("CONSULT_OFFER_TEXT"),
        reply_markup=kb
    )

    # --- FSM TRANSITION (FINAL STEP) ---
    await set_state(user_id, "course_offer")