# src/handlers/admin.py

from telebot.types import Message, CallbackQuery
from src.common import bot
from src.config import ADMIN_IDS
from src.keyboards.inline_kb import (
    admin_main_kb,
    admin_payment_kb,
    admin_request_kb,
    admin_users_filter_kb
)
from src.utils.humanize import humanize, FORMAT_MAP, TERM_MAP, EXP_MAP, CONTRA_MAP
from src.utils.state_manager import get_applications, get_application, update_application


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

    apps = await get_applications(filter_status="new")
    if not apps:
        await bot.send_message(call.message.chat.id, "Новых заявок нет")
        return

    for app in apps:
        user = app["user"]
        text = (
            f"Заявка #{app['id']}\n\n"
            f"Пользователь: {user.get('first_name', '')} {user.get('last_name', '')}\n"
            f"Username: @{user.get('username', '—')}\n"
            f"Срок беременности: {humanize(app.get('pregnancy_term', ''), TERM_MAP)}\n"
            f"Опыт йоги: {humanize(app.get('yoga_experience', ''), EXP_MAP)}\n"
            f"Противопоказания: {humanize(app.get('contraindications', ''), CONTRA_MAP)}\n"
            f"Формат: {humanize(app.get('format', ''), FORMAT_MAP)}\n"
            f"Контакт: {app.get('contact', '—')}\n"
            f"Дата создания: {app.get('created_at', '')}\n"
            f"Статус: {app.get('status', '')}"
        )
        await bot.send_message(call.message.chat.id, text, reply_markup=admin_request_kb(app["id"]))


# -------------------- Actions on applications (Completed / Rejected) --------------------
@bot.callback_query_handler(func=lambda c: c.data.startswith("admin:req_"))
async def admin_request_action(call: CallbackQuery):
    if not is_admin(call.from_user.id):
        return

    parts = call.data.split(":")
    action = parts[1]  # req_done / req_reject
    app_id = int(parts[2])

    app = await get_application(app_id)
    if not app:
        await bot.answer_callback_query(call.id, "Заявка не найдена")
        return

    if action == "req_done":
        await update_application(app_id, {"status": "processed"})
    elif action == "req_reject":
        await update_application(app_id, {"status": "rejected"})

    await bot.edit_message_text(
        f"Заявка #{app_id}\nСтатус: {app['status']}",
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

    apps = await get_applications(filter_status="paid_pending")
    if not apps:
        await bot.send_message(call.message.chat.id, "Ожидающих оплат нет")
        return

    for app in apps:
        user = app["user"]
        text = (
            f"Оплата ожидает подтверждения\n\n"
            f"Пользователь: {user.get('first_name', '')} {user.get('last_name', '')}\n"
            f"Username: @{user.get('username', '—')}\n"
            f"Источник: {app.get('entry_point', '')}\n"
            f"Формат: {humanize(app.get('format', ''), FORMAT_MAP)}\n"
            f"Дата создания: {app.get('created_at', '')}"
        )
        await bot.send_message(call.message.chat.id, text, reply_markup=admin_payment_kb(app["id"]))


# -------------------- Payment confirmation / rejection --------------------
@bot.callback_query_handler(func=lambda c: c.data.startswith("admin:paid") or c.data.startswith("admin:not_paid"))
async def admin_payment_action(call: CallbackQuery):
    if not is_admin(call.from_user.id):
        return

    action, app_id = call.data.split(":")[1:]
    app_id = int(app_id)

    app = await get_application(app_id)
    if not app:
        await bot.answer_callback_query(call.id, "Заявка не найдена")
        return

    if action == "paid":
        await update_application(app_id, {"status": "paid"})
    elif action == "not_paid":
        await update_application(app_id, {"status": "rejected"})

    await bot.edit_message_text(
        f"Заявка #{app_id}\nСтатус: {app['status']}",
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
    apps = await get_applications(filter_type=filter_type)

    if not apps:
        await bot.send_message(call.message.chat.id, "Нет пользователей по выбранному фильтру")
        return

    for app in apps:
        user = app["user"]
        followup = "Нет follow-up" if app.get("followup_stage") == 99 else f"Этап: {app.get('followup_stage')}"
        text = (
            f"Пользователь: {user.get('first_name', '')} {user.get('last_name', '')}\n"
            f"Username: @{user.get('username', '—')}\n"
            f"Формат: {humanize(app.get('format', ''), FORMAT_MAP)}\n"
            f"Статус заявки: {app.get('status', '')}\n"
            f"Follow-up: {followup}\n"
            f"Источник: {app.get('entry_point', '')}\n"
            f"Контакт: {app.get('contact', '—')}\n"
            f"Дата создания: {app.get('created_at', '')}"
        )
        await bot.send_message(call.message.chat.id, text)