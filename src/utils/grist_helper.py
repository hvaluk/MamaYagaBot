# src/utils/grist_helper.py

from datetime import datetime, timezone
import json

from src.utils.grist_client import grist
from src.config import ADMIN_IDS, OWNER_IDS


# ===================== TIME =====================

def now_iso():
    return datetime.now(timezone.utc).isoformat()


# ===================== USERS =====================

async def get_grist_user(user_id: int):
    records = grist.fetch_all("Users")

    for rec in records:
        if str(rec.get("fields", {}).get("TelegramID")) == str(user_id):
            return rec.get("fields", {})   

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

async def create_user_message(user_row_id: int, application_id: int | None, message_text: str, state: str):

    if not user_row_id or not message_text:
        return None

    payload = {
        "User": user_row_id,
        "MessageText": message_text,
        "State": state,
        "CreatedAt": now_iso(),
        "status": "new"
       
    }

    if application_id:
        payload["Application"] = application_id

    return grist.insert("UserMessages", payload)


async def get_user_messages():
    records = grist.fetch_all("UserMessages")

    result = []
    for rec in records:
        result.append({
            "id": rec["id"],
            "fields": rec.get("fields", {})
        })

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