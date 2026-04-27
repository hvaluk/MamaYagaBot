# src/handlers/course/experience.py

from telebot.types import CallbackQuery
from src.common import bot
from src.keyboards.inline_kb import build_inline_kb
from src.config import settings
from src.utils.humanize import EXP_MAP
from src.utils.state_manager import get_state, set_state, update_application


@bot.callback_query_handler(func=lambda c: c.data in EXP_MAP)
async def course_experience(call: CallbackQuery):

    user_id = call.from_user.id
    chat_id = call.message.chat.id

    # --- STATE GUARD ---
    state = await get_state(user_id)
    if state != "course_experience":
        return await bot.answer_callback_query(call.id)

    await bot.answer_callback_query(call.id)

    # --- SAFE MAP ---
    value = EXP_MAP.get(call.data)
    if not value:
        return

    # --- SAVE DATA (ONLY DATA LAYER) ---
    await update_application(user_id, {
        "yoga_experience": value
    })

    # --- FSM TRANSITION (ONLY FLOW LAYER) ---
    await set_state(user_id, "course_request")

    # --- NEXT STEP UI ---
    kb = await build_inline_kb("request_kb")

    await bot.send_message(
        chat_id,
        settings.get_text("ASK_REQUEST"),
        reply_markup=kb
    )