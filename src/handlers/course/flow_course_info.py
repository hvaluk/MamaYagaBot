# src/handlers/course/flow_course_info.py

from telebot.types import CallbackQuery
from src.common import bot
from src.utils.state_manager import get_application, update_application
from src.keyboards.inline_kb import course_flow_info_kb
from src.config import settings


@bot.callback_query_handler(func=lambda c: c.data == "flow_info")
async def info_clicked(callback: CallbackQuery):

    user_id = callback.from_user.id
    chat_id = callback.message.chat.id

    # Fetch latest application asynchronously
    app = await get_application(user_id)

    if app:
        fields = app.get("fields", {})

        # If user is in trial and followup_stage is 0, advance stage to 1
        if fields.get("is_trial") and fields.get("followup_stage") == 0:
            await update_application(user_id, {"followup_stage": 1})

    # Send course info message
    await bot.send_message(
        chat_id,
        settings.get_text("ABOUT_PROGRAM"),  
    )