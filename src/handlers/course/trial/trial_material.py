# src/handlers/course/trial/trial_material.py

from telebot.types import CallbackQuery
from datetime import datetime

from src.common import bot
from src.config import settings
from src.config import MINSK_TZ
from src.utils.state_manager import get_application, update_application

@bot.callback_query_handler(func=lambda c: c.data == "trial_lect")
async def open_trial_material(callback: CallbackQuery):

    user_id = callback.from_user.id
    chat_id = callback.message.chat.id

    app = await get_application(user_id)
    if not app:
        return  # No application

    fields = {}
    if not app.get("fields", {}).get("trial_opened_at"):
        fields = {
            "is_trial": True,
            "trial_opened_at": datetime.now(MINSK_TZ).isoformat(),
            "followup_stage": 0,
            "followup_last_sent_at": None
        }
        await update_application(user_id, fields)

    await bot.send_message(chat_id, settings.TRIAL_MINI_COURSE)