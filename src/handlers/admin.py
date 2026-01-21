# src/handlers/admin.py

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from sqlalchemy import select
from src.common import bot
from src.config import ADMIN_IDS
from src.dao.models import AsyncSessionLocal, Application, User
from src.utils.humanize import FORMAT_MAP, TERM_MAP, EXP_MAP, CONTRA_MAP, humanize

# ---------------- Проверка прав администратора ----------------
def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

# ---------------- Клавиатура для действий с заявкой ----------------
def admin_request_kb(app_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("✔️ Выполнено", callback_data=f"req_done:{app_id}"),
        InlineKeyboardButton("❌ Отклонено", callback_data=f"req_reject:{app_id}")
    )
    return kb

# ---------------- Список последних заявок ----------------
@bot.message_handler(commands=["requests"])
async def cmd_requests(message: Message):
    if not is_admin(message.from_user.id):
        await bot.send_message(message.chat.id, "У вас нет доступа.")
        return

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Application)
            .order_by(Application.created_at.desc())
            .limit(20)
        )
        apps = result.scalars().all()

        for app in apps:
            user = await session.get(User, app.user_id)

            # Формат: "Не выбран", если пользователь не дошёл до выбора формата
            if not app.format or (app.format == "contra") or (app.contraindications in ("contra_yes", "contra_unsure") and app.current_step != "COURSE_FORMAT"):
                format_display = "Не выбран"
            else:
                format_display = humanize(app.format, FORMAT_MAP)

            contraindications_display = humanize(app.contraindications, CONTRA_MAP)
            term_display = humanize(app.pregnancy_term, TERM_MAP)
            experience_display = humanize(app.yoga_experience, EXP_MAP)
            contact_display = app.contact or "—"

            text = (
                f"📋 Заявка #{app.id}\n\n"
                f"👤 Пользователь: {user.first_name or ''} {user.last_name or ''}\n"
                f"🔗 Username: @{user.username or '—'}\n\n"
                f"🤰 Срок: {term_display}\n"
                f"🧘 Опыт: {experience_display}\n"
                f"⚠️ Противопоказания: {contraindications_display}\n"
                f"📚 Формат: {format_display}\n"
                f"📞 Контакт: {contact_display}\n"
                f"🕒 {app.created_at.strftime('%d.%m %H:%M')}\n"
                f"Статус: {app.status}"
            )

            await bot.send_message(message.chat.id, text, reply_markup=admin_request_kb(app.id))

# ---------------- Обновление статуса заявки ----------------
@bot.callback_query_handler(func=lambda c: c.data.startswith("req_"))
async def admin_request_action(call: CallbackQuery):
    if not is_admin(call.from_user.id):
        await bot.answer_callback_query(call.id, "Нет доступа")
        return

    action, app_id = call.data.split(":")
    app_id = int(app_id)

    async with AsyncSessionLocal() as session:
        application = await session.get(Application, app_id)
        if not application:
            await bot.answer_callback_query(call.id, "Заявка не найдена")
            return

        # Обновляем статус
        application.status = "done" if action == "req_done" else "rejected"
        await session.commit()

    # Обновляем текст сообщения
    await bot.edit_message_text(
        f"📋 Заявка #{app_id} — {application.status}",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id
    )

    await bot.answer_callback_query(
        call.id,
        f"Статус заявки обновлён: {application.status}"
    )
