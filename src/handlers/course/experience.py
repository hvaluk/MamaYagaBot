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

    # --- STATE CHECK ---
    state = await get_state(user_id)
    if state != "course_experience":
        return

    await bot.answer_callback_query(call.id)

    value = EXP_MAP[call.data]

    # --- UPDATE APPLICATION ---
    await update_application(user_id, {
        "yoga_experience": value
    })

    # --- NEXT STEP ---
    await set_state(user_id, "course_contra")

    # --- SEND MESSAGE ---
    if value in ["нет", "немного"]:
        text = settings.get_text("SAFE_TEXT")
    else:
        text = settings.get_text("SAFE_TEXT_EXPERIENCED")

    kb = await build_inline_kb("contra_kb")
    await bot.send_message(
        call.message.chat.id,
        text,
        reply_markup=kb
    )