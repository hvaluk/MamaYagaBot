# src/handlers/admin.py

from src.common import bot
from src.config import ADMIN_IDS
from src.dao.models import AsyncSessionLocal, Request, User
from src.utils.humanize import TERM_MAP, EXP_MAP, CONTRA_MAP, FORMAT_MAP, humanize


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


@bot.message_handler(commands=["requests"])
async def cmd_requests(message):
    if not is_admin(message.from_user.id):
        await bot.send_message(message.chat.id, "У вас нет доступа.")
        return

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            Request.__table__.select()
            .order_by(Request.created_at.desc())
            .limit(20)
        )
        requests = result.fetchall()

    if not requests:
        await bot.send_message(message.chat.id, "Нет заявок.")
        return

    for r in requests:
        async with AsyncSessionLocal() as session:
            user = await session.get(User, r.user_id)

        text = (
            "📋 Заявка\n\n"
            f"👤 Пользователь: {user.first_name or ''} {user.last_name or ''}\n"
            f"🔗 Username: @{user.username}\n\n"
            f"🤰 Срок: {humanize(user.pregnancy_term, TERM_MAP)}\n"
            f"🧘 Опыт: {humanize(user.yoga_experience, EXP_MAP)}\n"
            f"⚠️ Противопоказания: {humanize(user.contraindications, CONTRA_MAP)}\n"
            f"📚 Формат: {humanize(r.format_chosen, FORMAT_MAP)}\n"
            f"📞 Контакт: {user.phone or '—'}\n\n"
            f"🕒 {r.created_at.strftime('%d.%m %H:%M')}"
        )

        await bot.send_message(message.chat.id, text)

