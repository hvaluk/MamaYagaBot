# src/handlers/course/formats.py

from telebot.types import CallbackQuery

from src.common import bot
from src.dao.models import AsyncSessionLocal, User, Request
from src.states import get_state, set_state, clear_state, UserState

from src.texts.course import (
    FULL_COURSE_DESC,
    FULL_COURSE_PAYMENT,
    INDIVIDUAL_DESC,
    INDIVIDUAL_CLASS_CONSULT_TEXT,
    CONTACT_REQUEST
)


@bot.callback_query_handler(
    func=lambda c: c.data.startswith("fmt_")
    and get_state(c.from_user.id) == UserState.COURSE_FORMAT
)
async def course_format(callback: CallbackQuery):
    user_id = callback.from_user.id
    choice = callback.data  # fmt_course / fmt_individual / fmt_consult
    chat_id = callback.message.chat.id

    # --- сохраняем выбор ---
    async with AsyncSessionLocal() as session:
        user = await session.get(User, user_id)
        if not user:
            return

        session.add(
            Request(
                user_id=user.telegram_id,
                request_type="course_format",
                format_chosen=choice,
                payload=choice
            )
        )
        await session.commit()

    # --- сценарий ---
    if choice == "fmt_course":
        await bot.send_message(chat_id, FULL_COURSE_DESC)
        await bot.send_message(chat_id, FULL_COURSE_PAYMENT)
        clear_state(user_id)

    elif choice == "fmt_individual":
        await bot.send_message(chat_id, INDIVIDUAL_DESC)
        await bot.send_message(chat_id, CONTACT_REQUEST)
        set_state(user_id, UserState.COURSE_CONTACT)

    elif choice == "fmt_consult":
        await bot.send_message(chat_id, INDIVIDUAL_CLASS_CONSULT_TEXT)
        await bot.send_message(chat_id, CONTACT_REQUEST)
        set_state(user_id, UserState.COURSE_CONTACT)

    else:
        # защита от мусорных callback'ов
        clear_state(user_id)
