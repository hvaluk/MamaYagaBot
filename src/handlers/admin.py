# src/handlers/admin.py

import json
from telebot.types import Message, CallbackQuery
from src.common import bot
from src.config import ADMIN_IDS
from src.keyboards.inline_kb import build_inline_kb
from src.utils.grist_helper import (
    get_applications,
    get_grist_user_by_row_id,
    update_application_by_id,
    get_user_messages
)
from src.utils.humanize import format_human_datetime


# -------------------- Helpers --------------------
def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


# -------------------- /admin --------------------
@bot.message_handler(commands=["admin"])
async def admin_menu(message: Message):
    if not is_admin(message.from_user.id):
        return

    kb = await build_inline_kb("admin_main_kb")
    await bot.send_message(message.chat.id, "Админ-панель", reply_markup=kb)


# -------------------- REQUESTS --------------------
@bot.callback_query_handler(func=lambda c: c.data == "admin:requests")
async def admin_requests(call: CallbackQuery):
    if not is_admin(call.from_user.id):
        return

    await bot.answer_callback_query(call.id)

    # Новые заявки
    apps = await get_applications(filter_status="submitted")
    if not apps:
        await bot.send_message(call.message.chat.id, "Ожидающих заявок нет")
        return

    for app in apps:
        f = app["fields"]
        user = await get_grist_user_by_row_id(f.get("User"))

        created_at = format_human_datetime(f.get("created_at"))
        feelings_list = []
        try:
            feelings_list = json.loads(f.get("feelings") or "[]")
        except Exception:
            pass

        text = (
            f"Заявка #{app['id']}\n\n"
            f"Пользователь: {user.get('FirstName', '')} {user.get('LastName', '')}\n"
            f"Username: @{user.get('Username', '—')}\n"
            f"Telegram ID: {user.get('TelegramID', '—')}\n\n"
            f"Срок: {f.get('pregnancy_term', '—')}\n"
            f"Чувства: {', '.join(feelings_list) if feelings_list else '—'}\n"
            f"Опыт: {f.get('yoga_experience', '—')}\n"
            f"Запрос: {f.get('request_type', '—')}\n"
            f"Формат: {f.get('format', '—')}\n"
            f"Контакт: {f.get('contact', '—')}\n"
            f"Дата создания: {created_at}\n"
            f"Статус: {f.get('status', '—')}"
        )

        kb = await build_inline_kb("admin_request_kb", app_id=app["id"])
        await bot.send_message(call.message.chat.id, text, reply_markup=kb)


# -------------------- REQUEST ACTIONS --------------------
@bot.callback_query_handler(func=lambda c: c.data.startswith("admin:req_"))
async def admin_request_actions(call: CallbackQuery):
    if not is_admin(call.from_user.id):
        return

    _, action, app_id = call.data.split(":")
    app_id = int(app_id)

    # Меняем статус заявки
    if action == "req_done":
        await update_application_by_id(app_id, {"status": "done"})
        await bot.answer_callback_query(call.id, "Выполнено ✅")
    elif action == "req_reject":
        await update_application_by_id(app_id, {"status": "rejected"})
        await bot.answer_callback_query(call.id, "Отклонено ❌")

    # Удаляем старое сообщение
    try:
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception:
        pass

    # Отправляем оставшиеся заявки
    apps = await get_applications(filter_status="submitted")
    if not apps:
        await bot.send_message(call.message.chat.id, "Ожидающих заявок нет")
        return

    for app in apps:
        f = app["fields"]
        user = await get_grist_user_by_row_id(f.get("User"))
        created_at = format_human_datetime(f.get("created_at"))
        feelings_list = []
        try:
            feelings_list = json.loads(f.get("feelings") or "[]")
        except Exception:
            pass

        text = (
            f"Заявка #{app['id']}\n\n"
            f"Пользователь: {user.get('FirstName', '')} {user.get('LastName', '')}\n"
            f"Username: @{user.get('Username', '—')}\n"
            f"Telegram ID: {user.get('TelegramID', '—')}\n\n"
            f"Срок: {f.get('pregnancy_term', '—')}\n"
            f"Чувства: {', '.join(feelings_list) if feelings_list else '—'}\n"
            f"Опыт: {f.get('yoga_experience', '—')}\n"
            f"Запрос: {f.get('request_type', '—')}\n"
            f"Формат: {f.get('format', '—')}\n"
            f"Контакт: {f.get('contact', '—')}\n"
            f"Дата создания: {created_at}\n"
            f"Статус: {f.get('status', '—')}"
        )
        kb = await build_inline_kb("admin_request_kb", app_id=app["id"])
        await bot.send_message(call.message.chat.id, text, reply_markup=kb)


# -------------------- PAYMENTS --------------------
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
        f = app["fields"]
        user = await get_grist_user_by_row_id(f.get("User"))
        created_at = format_human_datetime(f.get("created_at"))

        text = (
            f"Оплата ожидает подтверждения\n\n"
            f"Пользователь: {user.get('FirstName', '')} {user.get('LastName', '')}\n"
            f"Username: @{user.get('Username', '—')}\n"
            f"Источник: {f.get('entry_point', '—')}\n"
            f"Формат: {f.get('format', '—')}\n"
            f"Дата создания: {created_at}"
        )

        kb = await build_inline_kb("admin_payment_kb", app_id=app["id"])
        await bot.send_message(call.message.chat.id, text, reply_markup=kb)


# -------------------- PAYMENT ACTIONS --------------------
@bot.callback_query_handler(func=lambda c: c.data.startswith("admin:paid") or c.data.startswith("admin:not_paid"))
async def admin_payment_actions(call: CallbackQuery):
    if not is_admin(call.from_user.id):
        return

    action, app_id = call.data.split(":")[1:]
    app_id = int(app_id)

    if action == "paid":
        await update_application_by_id(app_id, {"status": "paid"})
        await bot.answer_callback_query(call.id, "Оплачено ✅")
    elif action == "not_paid":
        await update_application_by_id(app_id, {"status": "rejected"})
        await bot.answer_callback_query(call.id, "Не оплачено ❌")

    # Обновляем список оплат
    try:
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception:
        pass

    apps = await get_applications(filter_status="paid_pending")
    if not apps:
        await bot.send_message(call.message.chat.id, "Ожидающих оплат нет")
        return

    for app in apps:
        f = app["fields"]
        user = await get_grist_user_by_row_id(f.get("User"))
        created_at = format_human_datetime(f.get("created_at"))

        text = (
            f"Оплата ожидает подтверждения\n\n"
            f"Пользователь: {user.get('FirstName', '')} {user.get('LastName', '')}\n"
            f"Username: @{user.get('Username', '—')}\n"
            f"Источник: {f.get('entry_point', '—')}\n"
            f"Формат: {f.get('format', '—')}\n"
            f"Дата создания: {created_at}"
        )
        kb = await build_inline_kb("admin_payment_kb", app_id=app["id"])
        await bot.send_message(call.message.chat.id, text, reply_markup=kb)


# -------------------- MESSAGES --------------------
@bot.callback_query_handler(func=lambda c: c.data == "admin:messages")
async def admin_messages(call: CallbackQuery):
    if not is_admin(call.from_user.id):
        return

    await bot.answer_callback_query(call.id)

    messages = await get_user_messages()
    if not messages:
        await bot.send_message(call.message.chat.id, "Сообщений нет")
        return

    for msg in messages:
        f = msg["fields"]
        user = await get_grist_user_by_row_id(f.get("User"))

        text = (
            f"Сообщение\n\n"
            f"Пользователь: {user.get('FirstName', '')} {user.get('LastName', '')}\n"
            f"Username: @{user.get('Username', '—')}\n\n"
            f"{f.get('MessageText', '')}"
        )
        await bot.send_message(call.message.chat.id, text)