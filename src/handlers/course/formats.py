# src/handlers/course/formats.py


from telebot import types
from telebot.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from src.common import bot
from src.keyboards.inline_kb import (
    formats_kb,
    course_options_kb,
    course_info_kb,
    individual_options_kb,
    consult_options_kb,
    trial_lesson_kb,
    contact_request_kb
)
from src.texts.course import (
    ONLINE_GROUP_CLASS_DESC,
    INDIVIDUAL_DESC,
    INDIVIDUAL_CLASS_CONSULT_TEXT,
    CONTACT_REQUEST
)
from src.states import get_state, set_state, UserState
from src.dao.models import AsyncSessionLocal, User, Request
from src.config import ONLINE_GROUP_PRICE_BYN, ONLINE_GROUP_PRICE_EUR

# ---------------- 1️⃣ Выбор формата ----------------
@bot.callback_query_handler(
    func=lambda c: c.data.startswith("fmt_")
    and get_state(c.from_user.id) == UserState.COURSE_FORMAT
)
async def choose_format(callback: CallbackQuery):
    await bot.answer_callback_query(callback.id)
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id

    async with AsyncSessionLocal() as session:
        user = await session.get(User, user_id)
        if not user:
            await bot.send_message(chat_id, "Произошла ошибка. Попробуйте снова.")
            return
        session.add(
            Request(
                user_id=user.telegram_id,
                request_type="format_chosen",
                format_chosen=callback.data,
                payload=callback.data
            )
        )
        await session.commit()

    # ---------------- Йога онлайн ----------------
    if callback.data == "fmt_course":
        set_state(user_id, UserState.COURSE_PAY)
        text = (
            f"Отлично! Ты выбрала Йога онлайн в группе.\n\n"
            f"Стоимость абонемента: {ONLINE_GROUP_PRICE_BYN} BYN / {ONLINE_GROUP_PRICE_EUR}€ 🔥\n\nЧто дальше?"
        )
        kb = course_options_kb()  # Оплатить, Узнать подробнее, Назад

    # ---------------- Индивидуальные занятия ----------------
    elif callback.data == "fmt_individual":
        set_state(user_id, UserState.COURSE_CONTACT)
        text = "Отлично! Ты выбрала индивидуальное занятие.\n\nЧто дальше?"
        kb = individual_options_kb()  

    # ---------------- Консультация ----------------
    else:  # fmt_consult
        set_state(user_id, UserState.COURSE_CONTACT)
        text = INDIVIDUAL_CLASS_CONSULT_TEXT
        kb = consult_options_kb()  # Записаться, Пробный урок, Назад

    await bot.send_message(chat_id, text, reply_markup=kb)

# ---------------- 2️⃣ Подробности курса (Йога онлайн) ----------------
@bot.callback_query_handler(func=lambda c: c.data == "course_info")
async def course_info(callback: CallbackQuery):
    await bot.answer_callback_query(callback.id)
    await bot.send_message(callback.message.chat.id, ONLINE_GROUP_CLASS_DESC, reply_markup=course_info_kb())

# ---------------- 3️⃣ Начать индивидуальное занятие ----------------
@bot.callback_query_handler(func=lambda c: c.data == "start_individual")
async def start_individual(callback: CallbackQuery):
    await bot.answer_callback_query(callback.id)

    text = (
        "Отличный выбор!\n\n"
        + INDIVIDUAL_DESC
        + CONTACT_REQUEST
    )

    await bot.send_message(
        callback.message.chat.id,
        text,
        reply_markup=contact_request_kb()  # 🔹 ReplyKeyboard
    )


# ---------------- 4️⃣ Узнать подробнее для индивидуальных занятий ----------------
@bot.callback_query_handler(func=lambda c: c.data == "individual_info")
async def individual_info(callback: CallbackQuery):
    await bot.answer_callback_query(callback.id)

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Начать заниматься", callback_data="start_individual"))
    kb.add(types.InlineKeyboardButton(
        "Записаться на бесплатное мини-занятие",
        callback_data="flow_trial"
    ))
    kb.add(types.InlineKeyboardButton("🔙 Назад", callback_data="fmt_individual"))

    await bot.send_message(
        callback.message.chat.id,
        INDIVIDUAL_DESC + CONTACT_REQUEST,
        reply_markup=kb
    )


# ---------------- 5️⃣ Пробный урок ----------------
@bot.callback_query_handler(func=lambda c: c.data == "flow_trial")
async def trial_lesson(callback: CallbackQuery):
    await bot.answer_callback_query(callback.id)
    from src.texts.common import TRIAL_OFFER
    await bot.send_message(callback.message.chat.id, TRIAL_OFFER, reply_markup=trial_lesson_kb())

# ---------------- 6️⃣ Отправка контакта ----------------
@bot.callback_query_handler(func=lambda c: c.data == "contact_request")
async def send_contact_request(callback: CallbackQuery):
    await bot.answer_callback_query(callback.id)
    await bot.send_message(callback.message.chat.id, CONTACT_REQUEST, reply_markup=contact_request_kb())
