# src/handlers/course/consult.py

from datetime import datetime
from telebot.types import CallbackQuery

from src.common import bot
from src.keyboards.inline_kb import build_inline_kb
from src.keyboards.reply_kb import build_reply_kb
from src.config import settings, MINSK_TZ
from src.utils.state_manager import set_state, update_application


# ------------------- OFFER ) -------------------
@bot.callback_query_handler(func=lambda c: c.data == "consult_offer")
async def consult_offer(call: CallbackQuery):
   
    await bot.answer_callback_query(call.id)

    user_id = call.from_user.id

    #  follow-up
    await update_application(user_id, {
        "is_trial": True,
        "followup_stage": 0,
        "followup_last_sent_at": datetime.now(MINSK_TZ).isoformat()
    })

    kb = await build_inline_kb("consult_offer_kb")

    await bot.send_message(
        call.message.chat.id,
        settings.get_text("CONSULT_OFFER_TEXT"),
        reply_markup=kb
    )


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


# ------------------- START (stop follow-up) -------------------
@bot.callback_query_handler(func=lambda c: c.data == "consult_start")
async def consult_start(call: CallbackQuery):
    await bot.answer_callback_query(call.id)

    user_id = call.from_user.id

    # full stop follow-up
    await update_application(user_id, {
        "format": "fmt_consult",
        "followup_stage": 99,
        "status": "contact_requested"
    })

    await set_state(user_id, "course_contact")

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

    user_id = call.from_user.id

    await set_state(user_id, "course_message")

    # restart follow-up
    await update_application(user_id, {
        "followup_stage": 0,
        "followup_last_sent_at": datetime.now(MINSK_TZ).isoformat()
    })

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

    user_id = call.from_user.id

    await set_state(user_id, "course_message")

    await bot.send_message(
        call.message.chat.id,
        settings.get_text("CONSULT_ASK_TEXT")
    )