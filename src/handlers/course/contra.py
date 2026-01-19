
# src/handlers/course/contra.py

from telebot.types import CallbackQuery
from src.common import bot
from src.dao.models import AsyncSessionLocal, User, Request
from src.keyboards.inline_kb import formats_kb
from src.texts.common import CONTRA_TEXT, FORMAT_TEXT
from src.states import set_state, UserState, get_state

@bot.callback_query_handler(
    func=lambda c: c.data.startswith("contra_")
    and get_state(c.from_user.id) == UserState.COURSE_CONTRA
)
async def course_contra(call: CallbackQuery):
    await bot.answer_callback_query(call.id)

    user_id = call.from_user.id
    value = call.data

    async with AsyncSessionLocal() as session:
        user = await session.get(User, user_id)
        user.contraindications = value

        session.add(Request(
            user_id=user.telegram_id,
            request_type="contraindications",
            payload=value
        ))
        await session.commit()

    if value == "contra_ok":
        set_state(user_id, UserState.COURSE_FORMAT)
        await bot.send_message(call.message.chat.id, FORMAT_TEXT, reply_markup=formats_kb())
    else:
        set_state(user_id, UserState.COURSE_CONTACT)
        await bot.send_message(call.message.chat.id, CONTRA_TEXT)
