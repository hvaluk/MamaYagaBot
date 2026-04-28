# src/handlers/admin.py

import json
from telebot.types import Message, CallbackQuery

from src.common import bot
from src.config import ADMIN_IDS
from src.keyboards.inline_kb import build_inline_kb

from src.utils.grist_helper import (
    get_applications,
    update_application_by_id,
    get_grist_user_by_row_id,   
    get_user_messages
)

from src.utils.humanize import format_human_datetime


# ---------------- AUTH ----------------
def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


# ---------------- HELPERS ----------------
def safe(v, default="—"):
    return v if v else default


def parse_json(value):
    try:
        data = json.loads(value or "[]")
        return data if isinstance(data, list) else []
    except:
        return []


# ---------------- MENU ----------------
@bot.message_handler(commands=["admin"])
async def admin_menu(message: Message):

    if not is_admin(message.from_user.id):
        return

    kb = await build_inline_kb("admin_main_kb")

    await bot.send_message(
        message.chat.id,
        "Админ-панель",
        reply_markup=kb
    )


# ---------------- REQUESTS ----------------
@bot.callback_query_handler(func=lambda c: c.data == "admin:requests")
async def admin_requests(call: CallbackQuery):

    if not is_admin(call.from_user.id):
        return

    await bot.answer_callback_query(call.id)

    apps = await get_applications(filter_status="submitted")

    if not apps:
        await bot.send_message(call.message.chat.id, "Новых заявок нет")
        return

    for app in apps:

        f = app.get("fields", {})
        user = await get_grist_user_by_row_id(f.get("User")) or {}
        
        feelings = parse_json(f.get("feelings"))

        text = (
            f"📩 Заявка #{app['id']}\n\n"
            f"Пользователь: {safe(user.get('FirstName'))} {safe(user.get('LastName'))}\n"
            f"Username: @{safe(user.get('Username'))}\n"
            f"Telegram ID: {safe(user.get('TelegramID'))}\n\n"
            f"Срок: {safe(f.get('pregnancy_term'))}\n"
            f"Чувства: {', '.join(feelings) if feelings else '—'}\n"
            f"Опыт: {safe(f.get('yoga_experience'))}\n"
            f"Запрос: {safe(f.get('request_type'))}\n"
            f"Контакт: {safe(f.get('contact'))}\n"
            f"Дата: {format_human_datetime(f.get('created_at'))}"
        )

        kb = await build_inline_kb("admin_request_kb", app_id=app["id"])

        await bot.send_message(call.message.chat.id, text, reply_markup=kb)


# ---------------- REQUEST ACTIONS ----------------
@bot.callback_query_handler(func=lambda c: c.data.startswith("admin:req_"))
async def admin_request_actions(call: CallbackQuery):

    if not is_admin(call.from_user.id):
        return

    await bot.answer_callback_query(call.id)

    try:
        _, action, app_id = call.data.split(":")
        app_id = int(app_id)
    except:
        return

    status_map = {
        "req_done": "done",
        "req_reject": "rejected"
    }

    if action in status_map:
        await update_application_by_id(app_id, {
            "status": status_map[action]
        })

    await bot.answer_callback_query(call.id, "Обновлено ✅")


# ---------------- MESSAGES ----------------
@bot.callback_query_handler(func=lambda c: c.data == "admin:messages")
async def admin_messages(call: CallbackQuery):

    if not is_admin(call.from_user.id):
        return

    await bot.answer_callback_query(call.id)

    messages = await get_user_messages()
    messages = [
        m for m in messages
        if m["fields"].get("status") not in ["answered"]
    ]


    if not messages:
        await bot.send_message(call.message.chat.id, "Новых сообщений нет")
        return

    for msg in messages:

        f = msg.get("fields", {})
        user = await get_grist_user_by_row_id(f.get("User")) or {}

        text = (
            f"💬 Сообщение #{msg['id']}\n\n"
            f"Пользователь: {safe(user.get('FirstName'))} {safe(user.get('LastName'))}\n"
            f"Username: @{safe(user.get('Username'))}\n"
            f"Telegram ID: {safe(user.get('TelegramID'))}\n\n"
            f"Статус: {safe(f.get('status'), 'new')}\n\n"
            f"{f.get('MessageText','')}"
        )

        kb = await build_inline_kb("admin_messages_kb", message_id=msg["id"])

        await bot.send_message(call.message.chat.id, text, reply_markup=kb)


# ---------------- MESSAGE ACTIONS ----------------
@bot.callback_query_handler(func=lambda c: c.data.startswith("admin:msg_"))
async def admin_message_actions(call: CallbackQuery):

    if not is_admin(call.from_user.id):
        return

    try:
        _, action, msg_id = call.data.split(":")
        msg_id = int(msg_id)
    except:
        await bot.answer_callback_query(call.id, "Ошибка")
        return

    status_map = {
        "msg_read": "read",
        "msg_answered": "answered",
    }

    new_status = status_map.get(action)

    if not new_status:
        await bot.answer_callback_query(call.id, "Неизвестное действие")
        return

    # --- UPDATE ---
    try:
        from src.utils.grist_client import grist

        grist.update("UserMessages", msg_id, {
            "status": new_status
        })
    except Exception as e:
        print("❌ UPDATE ERROR:", e)
        await bot.answer_callback_query(call.id, "Ошибка")
        return

    # --- FEEDBACK ---
    await bot.answer_callback_query(call.id, f"Статус: {new_status}")


    if new_status == "answered":
        try:
            await bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            pass