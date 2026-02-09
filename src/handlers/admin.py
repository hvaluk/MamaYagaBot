# src/handlers/admin.py

from telebot.types import  Message, CallbackQuery
from sqlalchemy import select
from src.common import bot
from src.config import ADMIN_IDS
from src.dao.models import AsyncSessionLocal, Application, User
from src.keyboards.inline_kb import (
    admin_main_kb,
    admin_payment_kb,
    admin_request_kb,
    admin_users_filter_kb
)
from src.utils.humanize import humanize, FORMAT_MAP, TERM_MAP, EXP_MAP, CONTRA_MAP

# -------------------- Helpers --------------------
def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

# -------------------- /admin --------------------
@bot.message_handler(commands=["admin"])
async def admin_menu(message: Message):
    if not is_admin(message.from_user.id):
        return
    await bot.send_message(
        message.chat.id,
        "Админ-панель",
        reply_markup=admin_main_kb()
    )

# -------------------- Applications --------------------
@bot.callback_query_handler(func=lambda c: c.data == "admin:requests")
async def admin_applications(call: CallbackQuery):
    if not is_admin(call.from_user.id):
        return
    await bot.answer_callback_query(call.id)

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Application)
            .where(Application.status == "new")
            .order_by(Application.created_at.desc())
        )
        apps = result.scalars().all()

        if not apps:
            await bot.send_message(call.message.chat.id, "Новых заявок нет")
            return

        for app in apps:
            user = await session.get(User, app.user_id)
            text = (
                f"Заявка #{app.id}\n\n"
                f"Пользователь: {user.first_name or ''} {user.last_name or ''}\n"
                f"Username: @{user.username or '—'}\n"
                f"Срок беременности: {humanize(app.pregnancy_term, TERM_MAP)}\n"
                f"Опыт йоги: {humanize(app.yoga_experience, EXP_MAP)}\n"
                f"Противопоказания: {humanize(app.contraindications, CONTRA_MAP)}\n"
                f"Формат: {humanize(app.format, FORMAT_MAP)}\n"
                f"Контакт: {app.contact or '—'}\n"
                f"Дата создания: {app.created_at.strftime('%d.%m %H:%M')}\n"
                f"Статус: {app.status}"
            )
            # Add Completed / Rejected buttons
            await bot.send_message(call.message.chat.id, text, reply_markup=admin_request_kb(app.id))

# -------------------- Actions on applications (Completed / Rejected) --------------------
@bot.callback_query_handler(func=lambda c: c.data.startswith("admin:req_"))
async def admin_request_action(call: CallbackQuery):
    if not is_admin(call.from_user.id):
        return

    parts = call.data.split(":")
    action = parts[1]  # req_done / req_reject
    app_id = int(parts[2])

    async with AsyncSessionLocal() as session:
        app = await session.get(Application, app_id)
        if not app:
            await bot.answer_callback_query(call.id, "Заявка не найдена")
            return

        if action == "req_done":
            app.status = "processed"
        elif action == "req_reject":
            app.status = "rejected"

        await session.commit()

    await bot.edit_message_text(
        f"Заявка #{app_id}\nСтатус: {app.status}",
        call.message.chat.id,
        call.message.message_id
    )
    await bot.answer_callback_query(call.id, "Статус обновлён")

# -------------------- Pending payments --------------------
@bot.callback_query_handler(func=lambda c: c.data == "admin:payments")
async def admin_payments(call: CallbackQuery):
    if not is_admin(call.from_user.id):
        return
    await bot.answer_callback_query(call.id)

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Application)
            .where(Application.status == "paid_pending")
            .order_by(Application.created_at.desc())
        )
        apps = result.scalars().all()

        if not apps:
            await bot.send_message(call.message.chat.id, "Ожидающих оплат нет")
            return

        for app in apps:
            user = await session.get(User, app.user_id)
            text = (
                f"Оплата ожидает подтверждения\n\n"
                f"Пользователь: {user.first_name or ''} {user.last_name or ''}\n"
                f"Username: @{user.username or '—'}\n"
                f"Источник: {app.entry_point}\n"
                f"Формат: {humanize(app.format, FORMAT_MAP)}\n"
                f"Дата создания: {app.created_at.strftime('%d.%m %H:%M')}"
            )
            # Add Paid / Not paid buttons
            await bot.send_message(call.message.chat.id, text, reply_markup=admin_payment_kb(app.id))

# -------------------- Payment confirmation / rejection --------------------
@bot.callback_query_handler(func=lambda c: c.data.startswith("admin:paid") or c.data.startswith("admin:not_paid"))
async def admin_payment_action(call: CallbackQuery):
    if not is_admin(call.from_user.id):
        return

    action, app_id = call.data.split(":")[1:]
    app_id = int(app_id)

    async with AsyncSessionLocal() as session:
        app = await session.get(Application, app_id)
        if not app:
            await bot.answer_callback_query(call.id, "Заявка не найдена")
            return

        if action == "paid":
            app.status = "paid"
        elif action == "not_paid":
            app.status = "rejected"

        await session.commit()

    await bot.edit_message_text(
        f"Заявка #{app_id}\nСтатус: {app.status}",
        call.message.chat.id,
        call.message.message_id
    )
    await bot.answer_callback_query(call.id, "Статус обновлён")

# -------------------- User management (main button) --------------------
@bot.callback_query_handler(func=lambda c: c.data == "admin:users")
async def admin_users(call: CallbackQuery):
    if not is_admin(call.from_user.id):
        return
    await bot.answer_callback_query(call.id)
    await bot.send_message(
        call.message.chat.id,
        "Выберите фильтр пользователей:",
        reply_markup=admin_users_filter_kb()
    )

# -------------------- User filters --------------------
@bot.callback_query_handler(func=lambda c: c.data.startswith("admin_users:"))
async def admin_users_filter(call: CallbackQuery):
    if not is_admin(call.from_user.id):
        return
    await bot.answer_callback_query(call.id)

    _, filter_type = call.data.split(":")

    async with AsyncSessionLocal() as session:
        query = select(Application)
        if filter_type == "new":
            query = query.where(Application.status == "new")
        elif filter_type == "paid_pending":
            query = query.where(Application.status == "paid_pending")
        elif filter_type == "paid":
            query = query.where(Application.status == "paid")
        elif filter_type == "followup":
            query = query.where(Application.followup_stage != 99)
        query = query.order_by(Application.created_at.desc())

        result = await session.execute(query)
        apps = result.scalars().all()

        if not apps:
            await bot.send_message(call.message.chat.id, "Нет пользователей по выбранному фильтру")
            return

        for app in apps:
            user = await session.get(User, app.user_id)
            followup = "Нет follow-up" if app.followup_stage == 99 else f"Этап: {app.followup_stage}"
            text = (
                f"Пользователь: {user.first_name or ''} {user.last_name or ''}\n"
                f"Username: @{user.username or '—'}\n"
                f"Формат: {humanize(app.format, FORMAT_MAP)}\n"
                f"Статус заявки: {app.status}\n"
                f"Follow-up: {followup}\n"
                f"Источник: {app.entry_point}\n"
                f"Контакт: {app.contact or '—'}\n"
                f"Дата создания: {app.created_at.strftime('%d.%m %H:%M')}"
            )
            await bot.send_message(call.message.chat.id, text)
