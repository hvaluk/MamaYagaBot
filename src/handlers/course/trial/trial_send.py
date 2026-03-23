# src/handlers/course/trial/trial_send.py

from telebot.types import CallbackQuery
from datetime import datetime, timezone

from src.common import bot
from src.config import settings
from src.keyboards.inline_kb import trial_lesson_kb
from src.utils.state_manager import update_application


@bot.callback_query_handler(func=lambda c: c.data == "flow_trial")
async def send_trial_lesson(callback: CallbackQuery):
    """
    Sends the trial lesson offer to the user.
    Marks the application as a trial and resets follow-up timestamps.
    """
    await bot.answer_callback_query(callback.id)
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id

    # Update the user's application: mark as trial, reset follow-up
    await update_application(user_id, {
        "is_trial": True,
        "followup_stage": 0,
        "followup_last_sent_at": None,
        "trial_opened_at": datetime.now(timezone.utc).isoformat()
    })

    # Send the trial offer message with inline keyboard
    await bot.send_message(
        chat_id,
        settings.get_text("TRIAL_OFFER"),
        reply_markup=trial_lesson_kb()
    ) 
