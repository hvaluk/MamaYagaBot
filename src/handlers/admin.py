# src/handlers/admin.py

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from src.common import bot
from src.config import ADMIN_IDS
from src.dao.models import AsyncSessionLocal, Request, User
from src.utils.humanize import TERM_MAP, EXP_MAP, CONTRA_MAP, FORMAT_MAP, humanize

# -----------------------------
# Проверка админа
# -----------------------------
def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

# -----------------------------
# Клавиатура для админа
# -----------------------------
def admin_request_kb(request_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("✔️ Выполнено", callback_data=f"req_done:{request_id}"),
        InlineKeyboardButton("❌ Отклонено", callback_data=f"req_reject:{request_id}")
    )
    return kb

# -----------------------------
# /requests — последние заявки
# -----------------------------
@bot.message_handler(commands=["requests"])
async def cmd_requests(message: Message):
    if not is_admin(message.from_user.id):
        await bot.send_message(message.chat.id, "У вас нет доступа.")
        return

    async with AsyncSessionLocal() as session:
        result = await session.execute(Request.__table__.select().order_by(Request.created_at.desc()).limit(20))
        requests = result.fetchall()
        if not requests:
            await bot.send_message(message.chat.id, "Нет заявок.")
            return

        user_ids = [r.user_id for r in requests]
        users = {uid: await session.get(User, uid) for uid in user_ids}

        for r in requests:
            user = users.get(r.user_id)
            if not user:
                continue
            text = (
                f"📋 Заявка #{r.id}\n\n"
                f"👤 Пользователь: {user.first_name or ''} {user.last_name or ''}\n"
                f"🔗 Username: @{user.username or '—'}\n\n"
                f"🤰 Срок: {humanize(user.pregnancy_term, TERM_MAP)}\n"
                f"🧘 Опыт: {humanize(user.yoga_experience, EXP_MAP)}\n"
                f"⚠️ Противопоказания: {humanize(user.contraindications, CONTRA_MAP)}\n"
                f"📚 Формат: {humanize(r.format_chosen, FORMAT_MAP)}\n"
                f"📞 Контакт: {user.phone or '—'}\n"
                f"🕒 {r.created_at.strftime('%d.%m %H:%M')}\n"
                f"Статус: {r.status or 'новая'}"
            )
            await bot.send_message(message.chat.id, text, reply_markup=admin_request_kb(r.id))

# -----------------------------
# Callback для изменения статуса заявки
# -----------------------------
@bot.callback_query_handler(func=lambda c: c.data.startswith("req_"))
async def admin_request_action(call: CallbackQuery):
    if not is_admin(call.from_user.id):
        await bot.answer_callback_query(call.id, "Нет доступа")
        return
    try:
        action, req_id_str = call.data.split(":")
        req_id = int(req_id_str)
        if action not in ("req_done", "req_reject"):
            await bot.answer_callback_query(call.id, "Некорректное действие")
            return
    except Exception:
        await bot.answer_callback_query(call.id, "Ошибка данных")
        return

    async with AsyncSessionLocal() as session:
        req = await session.get(Request, req_id)
        if not req:
            await bot.answer_callback_query(call.id, "Заявка не найдена")
            return
        req.status = "done" if action == "req_done" else "rejected"
        await session.commit()

    await bot.edit_message_text(
        f"Заявка #{req_id} — {req.status}",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id
    )
    await bot.answer_callback_query(call.id, f"Статус заявки обновлен: {req.status}")
