# src/handlers/course/experience.py

from telebot.types import CallbackQuery
from src.common import bot
from src.dao.models import AsyncSessionLocal, User, Request
from src.keyboards.inline_kb import contra_kb
from src.texts.common import SAFE_TEXT_EXPERIENCED
from src.states import set_state, get_state, UserState


EXP_MAP = {
    "exp_none": "нет",
    "exp_some": "немного",
    "exp_regular": "регулярно",
}


@bot.callback_query_handler(
    func=lambda c: c.data in EXP_MAP and get_state(c.from_user.id) == UserState.COURSE_EXPERIENCE
)
async def course_experience(call: CallbackQuery):
    experience = EXP_MAP[call.data]

    async with AsyncSessionLocal() as session:
        user = await session.get(User, call.from_user.id)
        user.yoga_experience = experience
        session.add(Request(
            user_id=user.telegram_id,
            request_type="yoga_experience",
            payload=experience
        ))
        await session.commit()

    await bot.send_message(call.message.chat.id, SAFE_TEXT_EXPERIENCED, reply_markup=contra_kb())
    set_state(call.from_user.id, UserState.COURSE_CONTRA)
