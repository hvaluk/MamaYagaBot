# src/handlers/course_flow.py

from src.common import bot
from src.dao.models import AsyncSessionLocal, User, Request
from src.keyboards.inline_kb import (
    pregnancy_kb,
    experience_kb,
    contra_kb,
    formats_kb,
    course_options_kb
)
from telebot.types import CallbackQuery
from src.config import OWNER_IDS, COURSE_PAY_LINK, COURSE_PRICE_BYN, COURSE_PRICE_EUR

# --- 1. Start Course ---
@bot.callback_query_handler(func=lambda c: c.data == "start_course_flow")
async def start_course(callback: CallbackQuery):
    await bot.send_message(
        callback.message.chat.id,
        "Отлично! Подберу для тебя безопасный и подходящий формат занятий 🙏\n\n"
        "Подскажи, какой у тебя срок беременности?",
        reply_markup=pregnancy_kb()
    )

# --- 2. Pregnancy Term ---
@bot.callback_query_handler(func=lambda c: c.data.startswith("term_"))
async def save_pregnancy_term(callback: CallbackQuery):
    term_map = {
        "term_0_12": "до 12 недель",
        "term_12_29": "12–29 недель",
        "term_30_38": "30–38 недель",
        "term_38_plus": "38+ недель"
    }

    async with AsyncSessionLocal() as session:
        user = await session.get(User, callback.from_user.id)
        if not user:
            return  # защита на случай, если user не найден
        user.pregnancy_term = term_map[callback.data]
        session.add(user)
        await session.commit()

        # Создаем запись Request для отслеживания
        req = Request(user_id=user.telegram_id, request_type="pregnancy_term", payload=user.pregnancy_term)
        session.add(req)
        await session.commit()

    await bot.send_message(
        callback.message.chat.id,
        "Здорово! Еще один уточняющий вопрос:\nТы раньше пробовала заниматься йогой?",
        reply_markup=experience_kb()
    )

# --- 3. Yoga Experience ---
@bot.callback_query_handler(func=lambda c: c.data.startswith("exp_"))
async def save_experience(callback: CallbackQuery):
    exp_map = {
        "exp_none": "нет",
        "exp_some": "немного",
        "exp_regular": "регулярно"
    }

    async with AsyncSessionLocal() as session:
        user = await session.get(User, callback.from_user.id)
        if not user:
            return
        user.yoga_experience = exp_map[callback.data]
        session.add(user)
        await session.commit()

        # Создаем запись Request для отслеживания
        req = Request(user_id=user.telegram_id, request_type="yoga_experience", payload=user.yoga_experience)
        session.add(req)
        await session.commit()

    if callback.data in ("exp_none", "exp_some"):
        text = (
            "Спасибо за твои ответы 💛\n"
            "Все практики безопасны даже если ты никогда не занималась йогой.\n"
            "Если нет медицинских противопоказаний — добро пожаловать на коврик 🧘‍♀️"
        )
        await bot.send_message(callback.message.chat.id, text, reply_markup=contra_kb())
    else:
        await bot.send_message(callback.message.chat.id, "Есть ли противопоказания?", reply_markup=contra_kb())

# --- 4. Contraindications ---
@bot.callback_query_handler(func=lambda c: c.data.startswith("contra_"))
async def save_contra(callback: CallbackQuery):
    async with AsyncSessionLocal() as session:
        user = await session.get(User, callback.from_user.id)
        if not user:
            return
        user.contraindications = callback.data
        session.add(user)
        await session.commit()

        # Создаем запись Request для отслеживания
        req = Request(user_id=user.telegram_id, request_type="contraindications", payload=user.contraindications)
        session.add(req)
        await session.commit()

    if callback.data in ("contra_yes", "contra_unsure"):
        for owner in OWNER_IDS:
            await bot.send_message(
                owner,
                f"⚠️ Пользователь с противопоказаниями\n"
                f"@{user.username}\nСрок: {user.pregnancy_term}\nОпыт: {user.yoga_experience}\nПротивопоказания: {user.contraindications}"
            )
        await bot.send_message(callback.message.chat.id,
            "При противопоказаниях есть бережные практики.\nАнна напишет тебе лично 💛")
        return

    await bot.send_message(callback.message.chat.id,
        "Теперь выбери удобный формат занятий:", reply_markup=formats_kb())

# --- 5. Full Course ---
@bot.callback_query_handler(func=lambda c: c.data == "fmt_course")
async def course_full(callback: CallbackQuery):
    await bot.send_message(
        callback.message.chat.id,
        f"🎄 Полный курс до 31 декабря 2025\nСтоимость: {COURSE_PRICE_BYN} BYN / {COURSE_PRICE_EUR} €",
        reply_markup=course_options_kb()
    )

# ---Individual online session---
@bot.callback_query_handler(func=lambda c: c.data == "fmt_individual")
async def course_individual(callback: CallbackQuery):
    await bot.send_message(
        callback.message.chat.id,
        "Индивидуальные занятия онлайн — отличный способ получить персональное внимание и адаптированные практики.\n\n"
        "Анна свяжется с тобой для обсуждения деталей и записи на первое занятие. 💛"
    )

# --- 6. Payment ---
@bot.callback_query_handler(func=lambda c: c.data == "course_pay")
async def course_pay(callback: CallbackQuery):
    await bot.send_message(callback.message.chat.id,
        f"Переходи по ссылке для оплаты 👇\n{COURSE_PAY_LINK}")

# 