# src/handlers/course/formats.py

from telebot.types import CallbackQuery
from src.common import bot
from src.dao.models import AsyncSessionLocal, User, Request
from src.keyboards.inline_kb import course_options_kb
from src.states import get_state, set_state, UserState


@bot.callback_query_handler(
    func=lambda c: c.data.startswith("fmt_")
    and get_state(c.from_user.id) == UserState.COURSE_FORMAT
)
async def choose_format(callback: CallbackQuery):
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id

    async with AsyncSessionLocal() as session:
        user = await session.get(User, user_id)
        if not user:
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

    set_state(user_id, UserState.COURSE_PAY)

    if callback.data == "fmt_course":
        text = "Отлично! Ты выбрала комплексный курс."
    elif callback.data == "fmt_individual":
        text = "Отлично! Ты выбрала индивидуальные занятия онлайн."
    else:
        text = "Отлично! Ты выбрала консультацию онлайн."

    await bot.send_message(chat_id, text, reply_markup=course_options_kb())
