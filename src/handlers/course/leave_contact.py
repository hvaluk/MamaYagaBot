# src/handlers/course/leave_contact.py

from telebot.types import CallbackQuery
from src.common import bot
from src.config import settings
from src.keyboards.reply_kb import contact_request_kb
from src.utils.state_manager import set_state, update_application

@bot.callback_query_handler(func=lambda c: c.data == "leave_contact")
async def ask_contact(callback: CallbackQuery):
    """
    Handles the 'leave contact' action.
    Marks the current application as 'done' to stop follow-up,
    and prompts user to share their contact.
    """
    await bot.answer_callback_query(callback.id)
    user_id = callback.from_user.id

    # Stop follow-up for the current application
    await update_application(user_id, {"status": "done"})

    # Set state to COURSE_CONTACT to handle user input
    await set_state(user_id, "course_contact")

    # Send message prompting contact sharing
    await bot.send_message(
        callback.message.chat.id,
        settings.get_text("ASK_CONTACT"),  # Grist-driven text
        reply_markup=contact_request_kb()
    )