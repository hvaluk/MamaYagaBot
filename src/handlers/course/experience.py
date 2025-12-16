# src/handlers/course/experience.py

from telebot.types import CallbackQuery
from src.common import bot
from src.dao.models import AsyncSessionLocal, User, Request
from src.keyboards.inline_kb import contra_kb
from src.texts.common import SAFE_TEXT, SAFE_TEXT_EXPERIENCED

EXP_MAP = {
    "exp_none": "нет",
    "exp_some": "немного",
    "exp_regular": "регулярно",
}

@bot.callback_query_handler(func=lambda c: c.data.startswith("exp_"))
async def save_experience(callback: CallbackQuery):
    """Сохраняем опыт занятий йогой и переходим к противопоказаниям"""
    experience = EXP_MAP.get(callback.data)
    if not experience:
        return

    async with AsyncSessionLocal() as session:
        user = await session.get(User, callback.from_user.id)
        if not user:
            return

        user.yoga_experience = experience
        session.add_all([
            user,
            Request(
                user_id=user.telegram_id,
                request_type="yoga_experience",
                payload=experience
            )
        ])
        await session.commit()

    text = SAFE_TEXT_EXPERIENCED if callback.data == "exp_regular" else SAFE_TEXT

    await bot.send_message(
        callback.message.chat.id,
        text,
        reply_markup=contra_kb()
    )
