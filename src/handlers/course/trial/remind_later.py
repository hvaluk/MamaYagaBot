# src/handlers/course/trial/remind_later.py

from datetime import datetime, timezone
from telebot.types import CallbackQuery

from src.common import bot
from src.utils.state_manager import get_application, update_application

@bot.callback_query_handler(func=lambda c: c.data == "remind_later")
async def remind_later(callback: CallbackQuery):
  
    await bot.answer_callback_query(callback.id, "Хорошо, напомню через 3 дня 🕒")
    user_id = callback.from_user.id

    app = await get_application(user_id)
    if not app or app.get("followup_stage", 99) >= 99:
        return  # No active application or already completed

    await update_application(user_id, {
        "followup_stage": 3,  # Represents "remind in 3 days"
        "followup_last_sent_at": datetime.now(timezone.utc).isoformat()
    })