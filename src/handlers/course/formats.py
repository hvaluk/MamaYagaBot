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

    async with AsyncSessionLocal() as session:
        user = await session.get(User, user_id)
        if not user:
            return
        session.add(Request(user_id=user.telegram_id, request_type="format_chosen", payload=callback.data))
        await session.commit()

    set_state(user_id, UserState.COURSE_PAY)

    if callback.data == "fmt_course":
        await bot.send_message(callback.message.chat.id, "Отлично! Ты выбрала комплексный курс.", reply_markup=course_options_kb())
    elif callback.data == "fmt_individual":
        await bot.send_message(callback.message.chat.id, "Отлично! Ты выбрала индивидуальные занятия онлайн.", reply_markup=course_options_kb())
    elif callback.data == "fmt_consult":
        await bot.send_message(callback.message.chat.id, "Отлично! Ты выбрала консультацию онлайн.", reply_markup=course_options_kb())
