# src/handlers/course/formats.py

from telebot import types
from telebot.types import CallbackQuery
from src.common import bot
from src.keyboards.inline_kb import (
    individual_info_kb,
    course_options_kb,
    course_info_kb,
    individual_options_kb,
    consult_options_kb,
    trial_lesson_kb,
    course_flow_info_kb
)
from src.keyboards.reply_kb import contact_request_kb
from src.texts.course import (
    ONLINE_GROUP_CLASS_DESC,
    INDIVIDUAL_DESC,
    INDIVIDUAL_CLASS_CONSULT_TEXT,
    CONTACT_REQUEST
)
from src.states import get_state, set_state, get_context, UserState
from src.dao.models import AsyncSessionLocal, Application
from src.config import ONLINE_GROUP_PRICE_BYN, ONLINE_GROUP_PRICE_EUR
from src.utils.followup import schedule_followup
from src.texts.common import TRIAL_OFFER, FOLLOWUP_FIRST, FOLLOWUP_24H


# ----------------  Выбор формата ----------------
@bot.callback_query_handler(func=lambda c: c.data.startswith("fmt_"))

async def choose_format(callback: CallbackQuery):
    await bot.answer_callback_query(callback.id)

    user_id = callback.from_user.id
    chat_id = callback.message.chat.id
    ctx = get_context(user_id)

    async with AsyncSessionLocal() as session:
        application = await session.get(Application, ctx["application_id"])
        application.format = callback.data
        await session.commit()

    # ---------------- Йога онлайн ----------------
    if callback.data == "fmt_course":
        set_state(user_id, UserState.COURSE_PAY)
        text = (
            f"Отлично! Ты выбрала Йога онлайн в группе.\n"
            f"Стоимость абонемента: {ONLINE_GROUP_PRICE_BYN} BYN / {ONLINE_GROUP_PRICE_EUR}€ 🔥\n\nЧто дальше?"
        )
        kb = course_options_kb()  # Оплатить, Узнать подробнее, Назад

    # ---------------- Индивидуальные занятия ----------------
    elif callback.data == "fmt_individual":
        set_state(user_id, UserState.COURSE_CONTACT)
        text = "Отлично! Ты выбрала индивидуальное занятие.\nЧто дальше?"
        kb = individual_options_kb()

    # ---------------- Консультация ----------------
    else:  # fmt_consult
        set_state(user_id, UserState.COURSE_CONTACT)
        text = INDIVIDUAL_CLASS_CONSULT_TEXT
        kb = consult_options_kb()  

    await bot.send_message(chat_id, text, reply_markup=kb)


# ---------------- Подробности курса (Йога онлайн) ----------------
@bot.callback_query_handler(func=lambda c: c.data == "flow_course_info")
async def cflow_course_info(callback: CallbackQuery):
    await bot.answer_callback_query(callback.id)
    await bot.send_message(
        callback.message.chat.id,
        ONLINE_GROUP_CLASS_DESC,
        reply_markup=course_info_kb()
    )


# ---------------- Начать индивидуальное занятие ----------------
@bot.callback_query_handler(func=lambda c: c.data == "start_individual")
async def start_individual(callback: CallbackQuery):
    await bot.answer_callback_query(callback.id)

    text = f"{INDIVIDUAL_DESC}{CONTACT_REQUEST}"

    await bot.send_message(
        callback.message.chat.id,
        text, parse_mode='Markdown',
        reply_markup=contact_request_kb() 
    )


# ----------------  Узнать подробнее для индивидуальных занятий ----------------
@bot.callback_query_handler(func=lambda c: c.data == "individual_info")
async def individual_info(callback: CallbackQuery):
    await bot.answer_callback_query(callback.id)

    await bot.send_message(
        callback.message.chat.id,
        f"{INDIVIDUAL_DESC}{CONTACT_REQUEST}",
        parse_mode='Markdown',
        reply_markup=individual_info_kb()
    )

# ----------------  Записаться на консультацию ----------------
@bot.callback_query_handler(func=lambda c: c.data == "start_consultation")
async def start_consultation(callback: CallbackQuery):
    await bot.answer_callback_query(callback.id)
    await bot.send_message(
        callback.message.chat.id,
        CONTACT_REQUEST,
        parse_mode='Markdown',
        reply_markup=contact_request_kb()
    )
