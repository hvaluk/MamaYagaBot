# src/handlers/course/flow_course_info.py

from telebot.types import CallbackQuery
from src.common import bot
from src.dao.models import AsyncSessionLocal
from src.keyboards.inline_kb import course_flow_info_kb
from src.texts.course import ABOUT_PROGRAM
from src.states import set_context, set_state, UserState


async def get_last_app(session, user_id):
    """
    Placeholder helper that returns the last application for a user or None.
    Replace with real DB query logic if needed (e.g. using SQLAlchemy select on your Application model).
    """
    return None


@bot.callback_query_handler(func=lambda c: c.data == "flow_info")
async def info_clicked(callback):
    async with AsyncSessionLocal() as session:
        app = await get_last_app(session, callback.from_user.id)

        if app and app.is_trial and app.followup_stage == 0:
            app.followup_stage = 1  # пропускаем 60 минут
            await session.commit()

    # дальше обычный сценарий
    await bot.send_message(
        callback.message.chat.id,
        ABOUT_PROGRAM,
        reply_markup=course_flow_info_kb()
    )
