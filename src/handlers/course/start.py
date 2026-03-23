# src/handlers/course/start.py

from telebot.types import CallbackQuery
from src.common import bot
from src.keyboards.inline_kb import build_inline_kb
from src.config import settings
from src.utils.grist_helper import create_application
from src.utils.state_manager import set_state

@bot.callback_query_handler(func=lambda c: c.data == "flow_trial_start")
async def start_course_flow(call: CallbackQuery):
    user_id = call.from_user.id

    # --- CREATE NEW APPLICATION ---
    await create_application(user_id, {
        "entry_point": "course",
        "is_trial": False,
        "current_step": "course_term"
    })

    # --- SET STATE ---
    await set_state(user_id, "course_term")

    # --- SEND FIRST QUESTION: срок беременности ---
    kb = await build_inline_kb("pregnancy_kb")
    await bot.send_message(
        call.message.chat.id,
        settings.get_text("ASK_TERM"),
        reply_markup=kb
    )