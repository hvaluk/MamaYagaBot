# src/handlers/course/consult.py

from telebot.types import CallbackQuery
from src.common import bot
from src.keyboards.inline_kb import build_inline_kb
from src.keyboards.reply_kb import build_reply_kb
from src.config import settings
from src.utils.state_manager import set_state

# ------------------- Learn More -------------------
@bot.callback_query_handler(func=lambda c: c.data == "consult_info")
async def consult_info(call: CallbackQuery):
    """
    Handler for 'Learn more' button (consult_info_kb)
    Shows detailed info about mini consultation.
    """
    await bot.answer_callback_query(call.id)

    kb = await build_inline_kb("consult_info_kb")
    await bot.send_message(
        call.message.chat.id,
        settings.get_text("CONSULT_INFO"),
        reply_markup=kb
    )

# ------------------- Start Consultation -------------------
@bot.callback_query_handler(func=lambda c: c.data == "consult_start")
async def consult_start(call: CallbackQuery):
    """
    Handler for 'Sign up for mini consultation' button
    Moves user to contact request state (course_contact)
    """
    await bot.answer_callback_query(call.id)

    await set_state(call.from_user.id, "course_contact")

    kb = await build_reply_kb("contact_request_kb")
    await bot.send_message(
        call.message.chat.id,
        settings.get_text("CONTACT_REQUEST"),
        reply_markup=kb
    )

# ------------------- Not Ready / Later -------------------
@bot.callback_query_handler(func=lambda c: c.data == "consult_later")
async def consult_later(call: CallbackQuery):
    """
    Handler for 'Not ready' button (consult_info_kb)
    Shows a reassuring message and repeats consult offer buttons
    """
    await bot.answer_callback_query(call.id)

    text = settings.get_text("CONSULT_LATER_TEXT")
    kb = await build_inline_kb("consult_offer_kb")
    await bot.send_message(call.message.chat.id, text, reply_markup=kb)