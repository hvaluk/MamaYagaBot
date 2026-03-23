# src/handlers/course/formats.py

from telebot.types import CallbackQuery
from src.common import bot
from src.config import settings

from src.utils.state_manager import get_state, set_state, update_application

from src.keyboards.inline_kb import (
    individual_info_kb,
    course_options_kb,
    course_info_kb,
    individual_options_kb,
    consult_options_kb,
)

from src.keyboards.reply_kb import contact_request_kb


# ---------------- Select class format ----------------
@bot.callback_query_handler(func=lambda c: c.data.startswith("fmt_"))
async def choose_format(callback: CallbackQuery):

    user_id = callback.from_user.id

    # --- STATE CHECK ---
    state = await get_state(user_id)
    if state != "course_format":
        return

    await bot.answer_callback_query(callback.id)

    chat_id = callback.message.chat.id

    if callback.data == "fmt_course":
        await update_application(user_id, {
            "format": "course"
        })

        await set_state(user_id, "course_pay")

        text = settings.get_text("ONLINE_GROUP_CLASS_DESC")

        kb = course_options_kb()

    elif callback.data == "fmt_individual":
        await update_application(user_id, {
            "format": "individual"
        })

        await set_state(user_id, "course_contact")

        text = settings.get_text("INDIVIDUAL_DESC")

        kb = individual_options_kb()

    else:  # fmt_consult
        await update_application(user_id, {
            "format": "consult"
        })

        await set_state(user_id, "course_contact")

        text = settings.get_text("INDIVIDUAL_CLASS_CONSULT_TEXT")

        kb = consult_options_kb()

    await bot.send_message(chat_id, text, reply_markup=kb)


# ---------------- Course details ----------------
@bot.callback_query_handler(func=lambda c: c.data == "flow_course_info")
async def cflow_course_info(callback: CallbackQuery):

    await bot.answer_callback_query(callback.id)

    await bot.send_message(
        callback.message.chat.id,
        settings.get_text("ONLINE_GROUP_CLASS_DESC"),
        reply_markup=course_info_kb()
    )


# ---------------- Start individual ----------------
@bot.callback_query_handler(func=lambda c: c.data == "start_individual")
async def start_individual(callback: CallbackQuery):

    await bot.answer_callback_query(callback.id)

    text = settings.get_text("INDIVIDUAL_DESC") + "\n\n" + settings.get_text("CONTACT_REQUEST")

    await bot.send_message(
        callback.message.chat.id,
        text,
        parse_mode="Markdown",
        reply_markup=contact_request_kb()
    )


# ---------------- Individual info ----------------
@bot.callback_query_handler(func=lambda c: c.data == "individual_info")
async def individual_info(callback: CallbackQuery):

    await bot.answer_callback_query(callback.id)

    text = settings.get_text("INDIVIDUAL_DESC") + "\n\n" + settings.get_text("CONTACT_REQUEST")

    await bot.send_message(
        callback.message.chat.id,
        text,
        parse_mode="Markdown",
        reply_markup=individual_info_kb()
    )


# ---------------- Consultation ----------------
@bot.callback_query_handler(func=lambda c: c.data == "start_consultation")
async def start_consultation(callback: CallbackQuery):

    await bot.answer_callback_query(callback.id)

    await bot.send_message(
        callback.message.chat.id,
        settings.get_text("CONTACT_REQUEST"),
        parse_mode="Markdown",
        reply_markup=contact_request_kb()
    )