# src/handlers/course/consult.py

from telebot.types import CallbackQuery
from src.common import bot
from src.keyboards.inline_kb import build_inline_kb
from src.keyboards.reply_kb import build_reply_kb
from src.config import settings
from src.utils.state_manager import set_state


# ------------------- INFO -------------------
@bot.callback_query_handler(func=lambda c: c.data == "consult_info")
async def consult_info(call: CallbackQuery):

    await bot.answer_callback_query(call.id)

    kb = await build_inline_kb("consult_info_kb")

    await bot.send_message(
        call.message.chat.id,
        settings.get_text("CONSULT_INFO"),
        reply_markup=kb
    )


# ------------------- START -------------------
@bot.callback_query_handler(func=lambda c: c.data == "consult_start")
async def consult_start(call: CallbackQuery):

    await bot.answer_callback_query(call.id)

    await set_state(call.from_user.id, "course_contact")

    kb = await build_reply_kb("contact_request_kb")

    await bot.send_message(
        call.message.chat.id,
        settings.get_text("CONTACT_REQUEST"),
        reply_markup=kb
    )


# ------------------- LATER -------------------
@bot.callback_query_handler(func=lambda c: c.data == "consult_later")
async def consult_later(call: CallbackQuery):

    await bot.answer_callback_query(call.id)

    await set_state(call.from_user.id, "course_message")

    kb = await build_inline_kb("consult_later_kb")

    await bot.send_message(
        call.message.chat.id,
        settings.get_text("CONSULT_LATER_TEXT"),
        reply_markup=kb
    )


# ------------------- ASK QUESTION -------------------
@bot.callback_query_handler(func=lambda c: c.data == "consult_ask")
async def consult_ask(call: CallbackQuery):

    await bot.answer_callback_query(call.id)

    await set_state(call.from_user.id, "course_message")

    await bot.send_message(
        call.message.chat.id,
        "Напиши свой вопрос 💛\nЯ передам его Анне и она лично тебе ответит"
    )