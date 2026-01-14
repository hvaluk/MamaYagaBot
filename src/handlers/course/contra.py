# src/handlers/course/contra.py

from telebot.types import CallbackQuery
from src.common import bot
from src.config import OWNER_IDS
from src.dao.models import AsyncSessionLocal, User, Request
from src.keyboards.inline_kb import formats_kb, leave_contact_kb
from src.texts.common import CONTRA_TEXT, FORMAT_TEXT
from src.states import get_state, set_state, UserState


@bot.callback_query_handler(
    func=lambda c: c.data.startswith("contra_")
    and get_state(c.from_user.id) == UserState.COURSE_CONTRA
)
async def course_contra(callback: CallbackQuery):
    user_id = callback.from_user.id

    # --- сохраняем ответ в БД ---
    async with AsyncSessionLocal() as session:
        user = await session.get(User, user_id)
        if not user:
            return

        user.contraindications = callback.data
        session.add(
            Request(
                user_id=user.telegram_id,
                request_type="contraindications",
                payload=callback.data
            )
        )
        await session.commit()

    # --- ветвление сценария ---
    if callback.data != "contra_ok":
        # есть противопоказания → контакт
        set_state(user_id, UserState.COURSE_CONTACT)
        await bot.send_message(
            callback.message.chat.id,
            CONTRA_TEXT,
            reply_markup=leave_contact_kb()
        )
    else:
        # всё ок → выбор формата
        set_state(user_id, UserState.COURSE_FORMAT)
        await bot.send_message(
            callback.message.chat.id,
            FORMAT_TEXT,
            reply_markup=formats_kb()
        )


# --- обработчик нажатия кнопки "Оставить контакт" ---
@bot.callback_query_handler(
    func=lambda c: c.data == "leave_contact"
    and get_state(c.from_user.id) == UserState.COURSE_CONTACT
)
async def save_contact(callback: CallbackQuery):
    user_id = callback.from_user.id

    async with AsyncSessionLocal() as session:
        user = await session.get(User, user_id)
        if not user:
            return

        # сохраняем факт запроса контакта
        session.add(
            Request(
                user_id=user.telegram_id,
                request_type="contact_request",
                payload="user_pressed_leave_contact"
            )
        )
        await session.commit()

    # уведомляем владельцев
    owner_message = (
        f"Новый контакт для обратной связи!\n\n"
        f"Пользователь: {user.first_name} {user.last_name or ''}\n"
        f"Telegram ID: @{user.username if user.username else user.telegram_id}\n"
        f"Состояние: {get_state(user_id)}"
    )
    for owner_id in OWNER_IDS:
        await bot.send_message(owner_id, owner_message)

    # подтверждение пользователю и перевод на выбор формата
    set_state(user_id, UserState.COURSE_FORMAT)
    await bot.send_message(
        callback.message.chat.id,
        FORMAT_TEXT,
        reply_markup=formats_kb()
    )
