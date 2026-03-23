# src/handlers/course/contra.py

from telebot.types import CallbackQuery
from src.common import bot
from src.config import settings

from src.utils.state_manager import get_state, set_state, update_application

from src.keyboards.inline_kb import build_inline_kb
from src.keyboards.reply_kb import build_reply_kb


@bot.callback_query_handler(func=lambda c: c.data.startswith("contra_"))
async def course_contra(call: CallbackQuery):

    user_id = call.from_user.id

    # --- STATE CHECK ---
    state = await get_state(user_id)
    if state != "course_contra":
        return

    await bot.answer_callback_query(call.id)

    value = call.data

    # --- UPDATE APPLICATION ---
    if value != "contra_ok":
        await update_application(user_id, {
            "contraindications": value,
            "format": "contra"
        })

        await set_state(user_id, "course_contact")

        kb = await build_inline_kb("contact_request_kb")
        await bot.send_message(
            call.message.chat.id,
            settings.get_text("CONTRA_TEXT"),
            reply_markup=kb
        )
        return

    # --- OK CASE ---
    await update_application(user_id, {
        "contraindications": value
    })

    await set_state(user_id, "course_format")

    kb = await build_inline_kb("formats_kb")
    await bot.send_message(
        call.message.chat.id,
        settings.get_text("FORMAT_TEXT"),
        reply_markup=kb
    )