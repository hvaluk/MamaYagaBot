# src/utils/grist_helper.py

import json
import asyncio
import requests
from datetime import datetime


from src.utils.grist_client import grist
from src.config import ADMIN_IDS, OWNER_IDS, MINSK_TZ


# ===================== TIME =====================

def now_iso():
    return datetime.now(MINSK_TZ).isoformat()


# ===================== USERS =====================

async def get_grist_user(user_id: int):
    records = grist.fetch_all("Users")

    for rec in records:
        if str(rec.get("fields", {}).get("TelegramID")) == str(user_id):
            return rec  

    return None


async def get_grist_user_by_row_id(row_id: int):
    if not row_id:
        return None

    records = grist.fetch_all("Users")

    for rec in records:
        if rec.get("id") == row_id:
            return rec.get("fields", {})  

    return None


async def create_user(user_obj):
    is_admin = user_obj.id in ADMIN_IDS or user_obj.id in OWNER_IDS

    grist.insert("Users", {
        "TelegramID": str(user_obj.id),
        "Username": user_obj.username or "",
        "FirstName": user_obj.first_name or "",
        "LastName": user_obj.last_name or "",
        "is_admin": is_admin,
        "is_active": True,
        "registered_at": now_iso()
    })

    return await get_grist_user(user_obj.id)


# ===================== APPLICATIONS =====================

async def create_application(user_id: int, fields: dict):
    records = grist.fetch_all("Users")

    user_row_id = None

    for rec in records:
        if str(rec.get("fields", {}).get("TelegramID")) == str(user_id):
            user_row_id = rec.get("id")
            break

    if not user_row_id:
        return None

    grist.insert("Applications", {
        "User": user_row_id,
        "entry_point": fields.get("entry_point", "course"),
        "is_trial": fields.get("is_trial", False),
        "current_step": fields.get("current_step", "start"),
        "status": "in_progress",
        "feelings": json.dumps(fields.get("feelings", []), ensure_ascii=False),
        "created_at": now_iso()
    })

    return await get_latest_application(user_id)


async def get_latest_application(user_id: int):
    user = await get_grist_user(user_id)
    if not user:
        return None

    records = grist.fetch_all("Applications")

    user_apps = [
        r for r in records
        if r.get("fields", {}).get("User") == user["id"]
    ]

    if not user_apps:
        return None

    return max(user_apps, key=lambda x: x["id"])


async def update_application(user_id: int, fields: dict):
    app = await get_latest_application(user_id)
    if not app:
        return False

    return grist.update("Applications", app["id"], fields)


async def update_application_by_id(app_id: int, fields: dict):
    if not app_id:
        return False

    return grist.update("Applications", app_id, fields)


async def get_applications(filter_status=None):
    records = grist.fetch_all("Applications")

    result = []
    for rec in records:
        fields = rec.get("fields", {})

        if filter_status and fields.get("status") != filter_status:
            continue

        result.append({
            "id": rec["id"],
            "fields": fields
        })

    return result


# ===================== USER MESSAGES =====================

def create_user_message(user_row_id, application_id, message_text, state):

    if not user_row_id or not message_text:
        return None

    payload = {
        "User": user_row_id,
        "Application": application_id,  
        "MessageText": message_text,
        "State": state,
        "CreatedAt": now_iso(),
        "status": "new"
    }

    print("📤 GRIST USER MESSAGE PAYLOAD:", payload)

    result = grist.insert("UserMessages", payload)

    print("📥 GRIST RESULT:", result)

    return result


async def get_user_messages(statuses=None):
    records = grist.fetch_all("UserMessages")

    result = []

    for rec in records:
        fields = rec.get("fields", {})

        status = (fields.get("status") or "new").lower()

        if statuses and status not in statuses:
            continue

        result.append({
            "id": rec["id"],
            "fields": fields
        })

    result.sort(key=lambda x: x["id"], reverse=True)

    return result

async def update_user_message(message_id: int, fields: dict):
    return grist.update("UserMessages", message_id, fields)


# ===================== BUTTONS =====================

async def get_buttons_for_keyboard(name: str) -> list[dict]:
    records = grist.fetch_all("Buttons")

    buttons = []

    for rec in records:
        fields = rec.get("fields", {})

        if fields.get("name") != name:
            continue

        buttons.append({
            "row_order": fields.get("row_order", 0),
            "label": fields.get("label"),
            "callback_data": fields.get("callback_data"),
            "request_contact": fields.get("request_contact", False)
        })

    return sorted(buttons, key=lambda x: x["row_order"])

## ===================== FOLLOW-UP =====================

async def get_followup_applications():
    records = grist.fetch_all("Applications")

    result = []

    for rec in records:
        fields = rec.get("fields", {})

        # Only applications in progress
        if fields.get("status") in ("done", "paid", "contact_requested"):
            continue

        if fields.get("followup_stage") == 99:
            continue

        result.append(rec)

    return result


async def update_application_by_row_id(row_id: int, fields: dict):
    if not row_id:
        return False

    return grist.update("Applications", row_id, fields)


async def get_telegram_id_by_user_row(user_row_id: int):
    records = grist.fetch_all("Users")

    for rec in records:
        if rec.get("id") == user_row_id:
            return rec.get("fields", {}).get("TelegramID")

    return None