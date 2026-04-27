# src/handlers/course/term.py

from telebot.types import CallbackQuery
from src.common import bot
from src.keyboards.inline_kb import build_inline_kb
from src.config import settings
from src.utils.state_manager import get_state, set_state, update_application
from src.utils.humanize import TERM_MAP


@bot.callback_query_handler(func=lambda c: c.data in TERM_MAP)
async def course_term(call: CallbackQuery):

    user_id = call.from_user.id
    chat_id = call.message.chat.id

    # --- STATE GUARD ---
    state = await get_state(user_id)
    if state != "course_term":
        return await bot.answer_callback_query(call.id)

    await bot.answer_callback_query(call.id)

    # --- SAFE MAP ---
    term = TERM_MAP.get(call.data)
    if not term:
        return

    # --- SAVE DATA ---
    await update_application(user_id, {
        "pregnancy_term": term
    })

    # --- NEXT STEP (ONLY state engine) ---
    await set_state(user_id, "course_feeling")

    # --- UI ---
    kb = await build_inline_kb("feeling_kb")

    await bot.send_message(
        chat_id,
        settings.get_text("ASK_FEELING"),
        reply_markup=kb
    )