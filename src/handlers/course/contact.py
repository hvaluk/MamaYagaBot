# src/handlers/course/contact.py

from telebot.types import Message, Contact, ReplyKeyboardRemove
from src.common import bot
from src.dao.models import AsyncSessionLocal, Application, User
from src.states import get_state, clear_state, get_context, UserState
from src.config import OWNER_IDS
from src.utils.humanize import humanize, TERM_MAP, EXP_MAP, CONTRA_MAP, FORMAT_MAP

@bot.message_handler(content_types=["text", "contact"])
async def receive_contact(message: Message):
    user_id = message.from_user.id

    if get_state(user_id) != UserState.COURSE_CONTACT:
        return

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

    ctx = get_context(user_id)

    async with AsyncSessionLocal() as session:
        application = await session.get(Application, ctx["application_id"])
        user = await session.get(User, user_id)

        application.contact = contact
        application.current_step = "COURSE_DONE"  # ✅ завершено
        await session.commit()

    await bot.send_message(
        message.chat.id,
        "Спасибо! 💛\nАнна свяжется с тобой в ближайшее время.",
        reply_markup=ReplyKeyboardRemove()
    )

    text = (
        f"📋 Заявка #{application.id}\n\n"
        f"👤 Пользователь: {user.first_name or ''} {user.last_name or ''}\n"
        f"🔗 Username: @{user.username or '—'}\n\n"
        f"🤰 Срок: {humanize(application.pregnancy_term, TERM_MAP)}\n"
        f"🧘 Опыт: {humanize(application.yoga_experience, EXP_MAP)}\n"
        f"⚠️ Противопоказания: {humanize(application.contraindications, CONTRA_MAP)}\n"
        f"📚 Формат: {humanize(application.format, FORMAT_MAP)}\n"
        f"📞 Контакт: {application.contact}\n\n"
        f"🕒 {application.created_at.strftime('%d.%m %H:%M')}"
    )

    for owner_id in OWNER_IDS:
        await bot.send_message(owner_id, text)

    clear_state(user_id)
