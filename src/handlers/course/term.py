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

    # --- STATE CHECK ---
    state = await get_state(user_id)
    if state != "course_term":
        return

    await bot.answer_callback_query(call.id)

    term = TERM_MAP[call.data]

    # --- UPDATE APPLICATION ---
    await update_application(user_id, {"pregnancy_term": term})

    # --- NEXT STEP ---
    await set_state(user_id, "course_feeling")

    # --- SEND NEXT QUESTION: состояние ---
    kb = await build_inline_kb("feeling_kb")
    await bot.send_message(
        call.message.chat.id,
        settings.get_text("ASK_FEELING"),
        reply_markup=kb
    )