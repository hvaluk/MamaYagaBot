# src/handlers/course/contact.py

from telebot.types import Message, Contact, ReplyKeyboardRemove
from sqlalchemy import select
from src.common import bot
from src.dao.models import AsyncSessionLocal, Application, User
from src.states import get_state, get_context, clear_state, UserState
from src.handlers.course.back import handle_back
from src.config import OWNER_IDS
from src.utils.humanize import humanize, TERM_MAP, EXP_MAP, CONTRA_MAP, FORMAT_MAP
from src.keyboards.reply_kb import contact_request_kb

FORBIDDEN_CONTACT_VALUES = {"назад", "back", "/start", "старт"}


@bot.message_handler(content_types=["text", "contact"])
async def receive_contact(message: Message):
    """
    Receives and processes user's contact information.
    """
    user_id = message.from_user.id
    chat_id = message.chat.id

    # state check
    if get_state(user_id) != UserState.COURSE_CONTACT:
        return

    # BACK
    if message.text and message.text.lower() == "назад":
        await handle_back(user_id, chat_id)
        return

    # contact extraction
    contact: str | None = None
    if message.contact and isinstance(message.contact, Contact):
        contact = message.contact.phone_number
    elif message.text:
        contact = message.text.strip()

    if not contact or len(contact) < 3 or contact.lower() in FORBIDDEN_CONTACT_VALUES:
        await bot.send_message(chat_id, "Пожалуйста, отправь номер телефона или Telegram @username 💛")
        return

    # retrieve application from context
    ctx = get_context(user_id)
    application_id = ctx.get("application_id")
    if not application_id:
        await bot.send_message(chat_id, "Ошибка. Попробуй начать заново 🙏")
        clear_state(user_id)
        return

    async with AsyncSessionLocal() as session:
        application = await session.get(Application, application_id)
        user = await session.get(User, user_id)
        if not application or not user:
            await bot.send_message(chat_id, "Ошибка. Попробуй начать заново 🙏")
            clear_state(user_id)
            return

        # application update
        application.contact = contact
        application.current_step = "COURSE_DONE"
        application.status = "done"
        await session.commit()

    # user message
    await bot.send_message(
        chat_id,
        "Спасибо! 💛\nАнна свяжется с тобой в ближайшее время.",
        reply_markup=ReplyKeyboardRemove()
    )
    clear_state(user_id)

    # admin notification
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
        try:
            await bot.send_message(owner_id, text)
        except Exception as e:
            print(f"Failed to notify owner {owner_id}: {e}")
