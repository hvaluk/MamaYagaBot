# src/handlers/course/leave_contact.py

from telebot.types import CallbackQuery
from src.common import bot
from src.config import settings
from src.keyboards.reply_kb import build_reply_kb
from src.utils.state_manager import set_state, update_application


@bot.callback_query_handler(func=lambda c: c.data == "leave_contact")
async def ask_contact(callback: CallbackQuery):
    await bot.answer_callback_query(callback.id)
    user_id = callback.from_user.id

    # --- STOP FOLLOW-UP ---
    await update_application(user_id, {"status": "done"})

    # --- SET STATE ---
    await set_state(user_id, "course_contact")

    # --- SEND CONTACT REQUEST ---
    kb = await build_reply_kb("contact_request_kb")
    await bot.send_message(
        callback.message.chat.id,
        settings.get_text("ASK_CONTACT"),
        reply_markup=kb
    )