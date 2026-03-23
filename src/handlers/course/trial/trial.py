# src/handlers/course/trial/trial.py


from telebot.types import CallbackQuery
from datetime import datetime, timezone
from src.common import bot
from src.config import settings
from src.keyboards.reply_kb import build_inline_kb
from src.utils.state_manager import set_state, update_application


@bot.callback_query_handler(func=lambda c: c.data == "flow_trial_start")
async def start_trial_flow(call: CallbackQuery):
    user_id = call.from_user.id

    # --- SET APPLICATION STATE ---
    await set_state(user_id, "course_term")
    await update_application(user_id, {
        "is_trial": True,
        "followup_stage": 0,
        "trial_opened_at": datetime.now(timezone.utc).isoformat()
    })

    # --- SEND NEXT KEYBOARD ---
    kb = await build_inline_kb("pregnancy_kb")
    await bot.send_message(
        call.message.chat.id,
        settings.get_text("ASK_TERM"),
        reply_markup=kb
    )


@bot.callback_query_handler(func=lambda c: c.data == "flow_trial")
async def trial_lesson(callback: CallbackQuery):
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id

    await update_application(user_id, {
        "is_trial": True,
        "followup_stage": 0,
        "trial_opened_at": datetime.now(timezone.utc).isoformat()
    })

    kb = await build_inline_kb("trial_lesson_kb")
    await bot.send_message(
        chat_id,
        settings.get_text("TRIAL_OFFER"),
        reply_markup=kb
    )