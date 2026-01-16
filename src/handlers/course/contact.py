# src/handlers/course/contact.py

from telebot.types import Message
from src.common import bot
from src.dao.models import AsyncSessionLocal, User, Request
from src.states import get_state, clear_state, UserState
from src.config import OWNER_IDS
from src.utils.humanize import humanize, TERM_MAP, EXP_MAP, CONTRA_MAP, FORMAT_MAP

@bot.message_handler(func=lambda m: get_state(m.from_user.id) == UserState.COURSE_CONTACT)
async def receive_contact(message: Message):
    user_id = message.from_user.id

    # Получаем контакт
    if message.contact and message.contact.phone_number:
        contact = message.contact.phone_number
    else:
        contact = (message.text or "").strip()

    if not contact:
        await bot.send_message(message.chat.id, "Пожалуйста, отправьте телефон или Telegram 💛")
        return

    async with AsyncSessionLocal() as session:
        user = await session.get(User, user_id)
        if not user:
            await bot.send_message(message.chat.id, "Произошла ошибка. Попробуйте снова.")
            return

        user.phone = contact

        # Создаем заявку
        r = Request(
            user_id=user.telegram_id,
            request_type="contact",
            payload=contact
        )
        session.add(r)
        await session.commit()

        # Формируем текст для владельцев (Анны)
        text = (
            "📋 Заявка\n\n"
            f"👤 Пользователь: {user.first_name or ''} {user.last_name or ''}\n"
            f"🔗 Username: @{user.username or '—'}\n\n"
            f"🤰 Срок: {humanize(user.pregnancy_term, TERM_MAP)}\n"
            f"🧘 Опыт: {humanize(user.yoga_experience, EXP_MAP)}\n"
            f"⚠️ Противопоказания: {humanize(user.contraindications, CONTRA_MAP)}\n"
            f"📚 Формат: {humanize(r.format_chosen, FORMAT_MAP)}\n"
            f"📞 Контакт: {user.phone or '—'}\n\n"
            f"🕒 {r.created_at.strftime('%d.%m %H:%M')}"
        )

    # Безопасная отправка каждому владельцу
    for owner_id in OWNER_IDS:
        try:
            await bot.send_message(owner_id, text)
        except Exception as e:
            print(f"Не удалось отправить владельцу {owner_id}: {e}")

    # Сообщение пользователю
    await bot.send_message(
        message.chat.id,
        "Спасибо! 💛\nАнна свяжется с тобой в ближайшее время."
    )

    # Очистка состояния
    clear_state(user_id)
