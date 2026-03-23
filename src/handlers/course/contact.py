# src/handlers/course/contact.py

from telebot.types import Message, Contact, ReplyKeyboardRemove
from src.common import bot
from src.config import OWNER_IDS
from src.utils.state_manager import get_state, set_state, get_application, update_application

FORBIDDEN_CONTACT_VALUES = {"назад", "back", "/start", "старт"}


@bot.message_handler(content_types=["text", "contact"])
async def receive_contact(message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    # --- STATE CHECK ---
    state = await get_state(user_id)
    if state != "course_contact":
        return

    # --- BACK ---
    if message.text and message.text.lower() == "назад":
        from src.handlers.course.back import handle_back
        await handle_back(user_id, chat_id)
        return

    # --- EXTRACT CONTACT ---
    contact: str | None = None
    if message.contact and isinstance(message.contact, Contact):
        contact = message.contact.phone_number
    elif message.text:
        contact = message.text.strip()

    if not contact or len(contact) < 3 or contact.lower() in FORBIDDEN_CONTACT_VALUES:
        await bot.send_message(chat_id, "Пожалуйста, отправь номер телефона или Telegram @username")
        return

    # --- GET APPLICATION ---
    app = await get_application(user_id)
    if not app:
        await bot.send_message(chat_id, "Ошибка. Попробуй начать заново")
        await set_state(user_id, "idle")
        return

    # --- UPDATE APPLICATION ---
    await update_application(app["id"], {
        "contact": contact,
        "current_step": "done",
        "status": "done"
    })

    # --- CONFIRM TO USER ---
    await bot.send_message(
        chat_id,
        "Спасибо! Ваш контакт сохранён.",
        reply_markup=ReplyKeyboardRemove()
    )
    await set_state(user_id, "idle")

    # --- ADMIN NOTIFICATION ---
    text = (
        f"Заявка #{app['id']}\n"
        f"Пользователь: {app.get('first_name', '')} {app.get('last_name', '')}\n"
        f"Username: @{app.get('username', '—')}\n"
        f"Срок: {app.get('pregnancy_term', '—')}\n"
        f"Опыт: {app.get('yoga_experience', '—')}\n"
        f"Противопоказания: {app.get('contraindications', '—')}\n"
        f"Формат: {app.get('format', '—')}\n"
        f"Контакт: {contact}\n"
        f"Дата создания: {app.get('created_at', '')}"
    )
    for owner_id in OWNER_IDS:
        try:
            await bot.send_message(owner_id, text)
        except Exception as e:
            print(f"Failed to notify owner {owner_id}: {e}")