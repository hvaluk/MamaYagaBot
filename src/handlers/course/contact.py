# src/handlers/course/contact.py

from telebot.types import Message, Contact, ReplyKeyboardRemove
from sqlalchemy import select, desc
from src.common import bot
from src.dao.models import AsyncSessionLocal, User, Request
from src.states import get_state, set_state, UserState
from src.config import OWNER_IDS
from src.utils.humanize import humanize, TERM_MAP, EXP_MAP, CONTRA_MAP, FORMAT_MAP

# Обрабатываем текст и контакт
@bot.message_handler(content_types=["text", "contact"])
async def receive_contact(message: Message):
    user_id = message.from_user.id

    # Проверяем состояние
    if get_state(user_id) != UserState.COURSE_CONTACT:
        return

    # Получаем контакт из кнопки или текста
    contact = None
    if message.contact and isinstance(message.contact, Contact):
        contact = message.contact.phone_number
    elif message.text:
        contact = message.text.strip()

    if not contact or len(contact) < 3:
        await bot.send_message(
            message.chat.id,
            "Пожалуйста, отправьте телефон или Telegram @username 💛"
        )
        return

    async with AsyncSessionLocal() as session:
        user = await session.get(User, user_id)
        if not user:
            await bot.send_message(message.chat.id, "Произошла ошибка. Попробуйте снова.")
            return

        user.phone = contact

        contact_request = Request(
            user_id=user.telegram_id,
            request_type="contact",
            payload=contact
        )
        session.add(contact_request)

        # 🔹 получаем последний выбранный формат
        result = await session.execute(
            select(Request)
            .where(
                Request.user_id == user.telegram_id,
                Request.request_type == "format_chosen"
            )
            .order_by(desc(Request.created_at))
            .limit(1)
        )
        format_request = result.scalar_one_or_none()

        # 🔹 определяем формат для заявки
        # Игнорируем старый выбор формата, если пользователь ещё не выбирал явно
        if format_request and get_state(user_id) != UserState.COURSE_FORMAT:
            format_value = "not_chosen"
        elif format_request:
            format_value = format_request.format_chosen
        else:
            format_value = "not_chosen"



        await session.commit()

    # Подтверждение пользователю + убираем клавиатуру
    await bot.send_message(
        message.chat.id,
        "Спасибо! 💛\nАнна свяжется с тобой в ближайшее время.",
        reply_markup=ReplyKeyboardRemove()
    )

    # Отправка админам
    text = (
        f"📋 Заявка\n\n"
        f"👤 Пользователь: {user.first_name or ''} {user.last_name or ''}\n"
        f"🔗 Username: @{user.username or '—'}\n\n"
        f"🤰 Срок: {humanize(user.pregnancy_term, TERM_MAP)}\n"
        f"🧘 Опыт: {humanize(user.yoga_experience, EXP_MAP)}\n"
        f"⚠️ Противопоказания: {humanize(user.contraindications, CONTRA_MAP)}\n"
        f"📚 Формат: {humanize(format_value, FORMAT_MAP)}\n"
        f"📞 Контакт: {user.phone or '—'}\n\n"
        f"🕒 {contact_request.created_at.strftime('%d.%m %H:%M')}"
    )
    for owner_id in OWNER_IDS:
        try:
            await bot.send_message(owner_id, text)
        except Exception as e:
            print(f"Не удалось отправить владельцу {owner_id}: {e}")

    # Сброс состояния
    set_state(user_id, UserState.NONE)
