# src/handlers/course/term.py

from telebot.types import CallbackQuery
from src.common import bot
from src.dao.models import AsyncSessionLocal, User, Request
from src.keyboards.inline_kb import experience_kb
from src.texts.common import ASK_EXPERIENCE
from src.states import set_state, get_state, UserState

TERM_MAP = {
    "term_0_12": "до 12 недель",
    "term_12_29": "12–29 недель",
    "term_30_38": "30–38 недель",
    "term_38_plus": "38+ недель",
}


@bot.callback_query_handler(
    func=lambda c: c.data in TERM_MAP and get_state(c.from_user.id) == UserState.COURSE_TERM
)
async def course_term(call: CallbackQuery):
    term = TERM_MAP[call.data]

    async with AsyncSessionLocal() as session:
        user = await session.get(User, call.from_user.id)
        user.pregnancy_term = term
        session.add(Request(
            user_id=user.telegram_id,
            request_type="pregnancy_term",
            payload=term
        ))
        await session.commit()

    await bot.send_message(call.message.chat.id, ASK_EXPERIENCE, reply_markup=experience_kb())
    set_state(call.from_user.id, UserState.COURSE_EXPERIENCE)
