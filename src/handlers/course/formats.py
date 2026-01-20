# src/handlers/course/formats.py

from telebot.types import CallbackQuery
from src.common import bot
from src.dao.models import AsyncSessionLocal, User, Request
from src.keyboards.inline_kb import course_options_kb
from src.keyboards.reply_kb import contact_request_kb
from src.texts.course import INDIVIDUAL_DESC, CONTACT_REQUEST, INDIVIDUAL_CLASS_CONSULT_TEXT
from src.states import get_state, set_state, UserState
from src.config import ONLINE_GROUP_PRICE_BYN, ONLINE_GROUP_PRICE_EUR

@bot.callback_query_handler(
    func=lambda c: c.data.startswith("fmt_")
    and get_state(c.from_user.id) == UserState.COURSE_FORMAT
)
async def choose_format(callback: CallbackQuery):
    await bot.answer_callback_query(callback.id)
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id

    async with AsyncSessionLocal() as session:
        user = await session.get(User, user_id)
        if not user:
            await bot.send_message(chat_id, "Произошла ошибка. Попробуйте снова.")
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

    if callback.data == "fmt_course":
        set_state(user_id, UserState.COURSE_PAY)
        text = f"Отлично! Ты выбрала Йога онлайн в группе.\n\n" \
               f"Стоимость абонемента: {ONLINE_GROUP_PRICE_BYN} BYN / {ONLINE_GROUP_PRICE_EUR}€ 🔥\n\nЧто дальше?"
        kb = course_options_kb()

    elif callback.data == "fmt_individual":
        set_state(user_id, UserState.COURSE_CONTACT)
        text = INDIVIDUAL_DESC + "\n\n" + CONTACT_REQUEST
        kb = contact_request_kb()  # Кнопка для отправки контакта

    else:  # fmt_consult
        set_state(user_id, UserState.COURSE_CONTACT)
        text = INDIVIDUAL_CLASS_CONSULT_TEXT + "\n\n" + CONTACT_REQUEST
        kb = contact_request_kb()  # Кнопка для отправки контакта

    await bot.send_message(chat_id, text, reply_markup=kb)
