# src/utils/grist_helper.py

import requests
import json
from datetime import datetime, timezone
from src.config import GRIST_BASE_URL, GRIST_DOC_ID, GRIST_API_KEY, ADMIN_IDS, OWNER_IDS

HEADERS = {
    "Authorization": f"Bearer {GRIST_API_KEY}",
    "Content-Type": "application/json"
}

def _url(table: str) -> str:
    return f"{GRIST_BASE_URL}{GRIST_DOC_ID}/tables/{table}/records"

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# -------------------- USERS --------------------
async def get_grist_user(user_id: int) -> dict | None:
    r = requests.get(_url("Users"), headers=HEADERS)
    r.raise_for_status()
    for rec in r.json().get("records", []):
        if str(rec["fields"].get("TelegramID")) == str(user_id):
            return rec
    return None

async def get_grist_user_by_row_id(row_id: int) -> dict:
    r = requests.get(_url("Users"), headers=HEADERS)
    r.raise_for_status()
    for rec in r.json().get("records", []):
        if rec["id"] == row_id:
            return rec["fields"]
    return {}

async def create_user(user_obj) -> dict:
    is_admin = user_obj.id in ADMIN_IDS or user_obj.id in OWNER_IDS
    payload = {
        "records": [{
            "fields": {
                "TelegramID": str(user_obj.id),
                "Username": user_obj.username or "",
                "FirstName": user_obj.first_name or "",
                "LastName": user_obj.last_name or "",
                "is_admin": is_admin,
                "is_active": True,
                "registered_at": now_iso()
            }
        }]
    }
    requests.post(_url("Users"), headers=HEADERS, json=payload).raise_for_status()
    return await get_grist_user(user_obj.id)


# -------------------- APPLICATIONS --------------------
async def create_application(user_id: int, fields: dict) -> dict | None:
    user = await get_grist_user(user_id)
    if not user:
        return None
    payload = {
        "records": [{
            "fields": {
                "User": user["id"],
                "entry_point": fields.get("entry_point", "course"),
                "pregnancy_term": fields.get("pregnancy_term", ""),
                "yoga_experience": fields.get("yoga_experience", ""),
                "request_type": fields.get("request_type", ""),
                "format": fields.get("format", ""),
                "contact": fields.get("contact", ""),
                "is_trial": fields.get("is_trial", False),
                "followup_stage": 0,
                "status": "submitted",
                "current_step": fields.get("current_step", "start"),
                "feelings": json.dumps(fields.get("feelings", [])),
                "created_at": now_iso()
            }
        }]
    }
    r = requests.post(_url("Applications"), headers=HEADERS, json=payload)
    r.raise_for_status()
    return r.json()

async def get_applications(filter_status: str | None = None) -> list[dict]:
    r = requests.get(_url("Applications"), headers=HEADERS)
    r.raise_for_status()
    result = []
    for rec in r.json().get("records", []):
        fields = rec["fields"]
        if filter_status and fields.get("status") != filter_status:
            continue
        result.append({"id": rec["id"], "fields": fields})
    return result

async def get_latest_application(user_id: int) -> dict | None:
    user = await get_grist_user(user_id)
    if not user:
        return None
    r = requests.get(_url("Applications"), headers=HEADERS)
    r.raise_for_status()
    records = [rec for rec in r.json().get("records", []) if rec["fields"].get("User") == user["id"]]
    if not records:
        return None
    latest = max(records, key=lambda x: x["id"])
    return latest

async def get_application_by_id(app_id: int) -> dict | None:
    r = requests.get(_url("Applications"), headers=HEADERS)
    r.raise_for_status()
    for rec in r.json().get("records", []):
        if rec["id"] == app_id:
            return rec
    return None

async def update_application(user_id: int, fields: dict) -> bool:
    app = await get_latest_application(user_id)
    if not app:
        return False
    payload = {"records": [{"id": app["id"], "fields": fields}]}
    requests.patch(_url("Applications"), headers=HEADERS, json=payload).raise_for_status()
    return True

async def update_application_by_id(app_id: int, fields: dict) -> bool:
    payload = {"records": [{"id": app_id, "fields": fields}]}
    requests.patch(_url("Applications"), headers=HEADERS, json=payload).raise_for_status()
    return True


# -------------------- BUTTONS --------------------
async def get_buttons_for_keyboard(name: str) -> list[dict]:
    r = requests.get(_url("Buttons"), headers=HEADERS)
    r.raise_for_status()
    buttons = []
    for rec in r.json().get("records", []):
        fields = rec["fields"]
        if fields.get("name") == name:
            buttons.append({
                "row_order": fields.get("row_order", 0),
                "label": fields.get("label"),
                "callback_data": fields.get("callback_data"),
                "request_contact": fields.get("request_contact", False)
            })
    return sorted(buttons, key=lambda x: x["row_order"])


# -------------------- USER MESSAGES --------------------
async def create_user_message(user_id: int, application_id: int | None, message_text: str, state: str):
    payload = {
        "records": [{
            "fields": {
                "User": user_id,
                "Application": application_id if application_id else None,
                "MessageText": message_text,
                "State": state,
                "CreatedAt": now_iso(),
                "AdminResponded": False
            }
        }]
    }
    r = requests.post(_url("UserMessages"), headers=HEADERS, json=payload)
    r.raise_for_status()
    return r.json()

async def get_user_messages(filter_state: str | None = None) -> list[dict]:
    r = requests.get(_url("UserMessages"), headers=HEADERS)
    r.raise_for_status()
    messages = []
    for rec in r.json().get("records", []):
        fields = rec["fields"]
        if filter_state and fields.get("State") != filter_state:
            continue
        messages.append({"id": rec["id"], "fields": fields})
    return messages