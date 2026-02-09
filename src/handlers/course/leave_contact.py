# src/handlers/course/leave_contact.py

from telebot.types import CallbackQuery
from sqlalchemy import select
from src.common import bot
from src.states import set_state, UserState
from src.keyboards.reply_kb import contact_request_kb
from src.dao.models import AsyncSessionLocal, Application

@bot.callback_query_handler(func=lambda c: c.data == "leave_contact")
async def ask_contact(callback: CallbackQuery):
    await bot.answer_callback_query(callback.id)
    user_id = callback.from_user.id

    # mark application status as "done" so the follow-up won't interfere
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Application)
            .where(Application.user_id == user_id)
            .order_by(Application.created_at.desc())
        )
        application = result.scalars().first()
        if application:
            application.status = "done"
            await session.commit()

    set_state(user_id, UserState.COURSE_CONTACT)

    await bot.send_message(
        callback.message.chat.id,
        "Оставь номер телефона кнопкой ниже или напиши свой Telegram @username 💛",
        reply_markup=contact_request_kb()
    )
