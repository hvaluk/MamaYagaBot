# src/utils/grist_helper.py

import requests
import json
from datetime import datetime, timezone

from src.config import (
    GRIST_BASE_URL,
    GRIST_DOC_ID,
    GRIST_API_KEY,
    ADMIN_IDS,
    OWNER_IDS
)

# -------------------- CONFIG --------------------

HEADERS = {
    "Authorization": f"Bearer {GRIST_API_KEY}",
    "Content-Type": "application/json"
}


def now() -> str:
    """Return current UTC datetime in ISO format"""
    return datetime.now(timezone.utc).isoformat()


def _url(table: str) -> str:
    """Build Grist API URL for table"""
    return f"{GRIST_BASE_URL}{GRIST_DOC_ID}/tables/{table}/records"


# -------------------- USERS --------------------

async def get_grist_user(user_id: int) -> dict | None:
    """
    Find user in Grist by TelegramID.
    Uses manual search to avoid type mismatch issues (int vs string).
    """
    r = requests.get(_url("Users"), headers=HEADERS)
    r.raise_for_status()

    records = r.json().get("records", [])

    for rec in records:
        if str(rec["fields"].get("TelegramID")) == str(user_id):
            return rec

    return None


async def create_user(user_obj) -> dict:
    """
    Create new user in Grist.
    Admin flag is determined from .env (ADMIN_IDS, OWNER_IDS).
    """
    is_admin = user_obj.id in ADMIN_IDS or user_obj.id in OWNER_IDS

    fields = {
        "TelegramID": str(user_obj.id),  # always store as string
        "Username": user_obj.username or "",
        "FirstName": user_obj.first_name or "",
        "LastName": user_obj.last_name or "",
        "is_admin": is_admin,
        "is_active": True,
        "registered_at": now()
    }

    payload = {"records": [{"fields": fields}]}

    r = requests.post(_url("Users"), headers=HEADERS, json=payload)
    r.raise_for_status()

    return await get_grist_user(user_obj.id)


# -------------------- APPLICATIONS --------------------

async def create_application(user_id: int, fields: dict) -> dict | None:
    """
    Create a new application linked to a user.
    """
    user = await get_grist_user(user_id)
    if not user:
        return None

    payload = {
        "records": [{
            "fields": {
                "User": user["id"],  # Reference column
                "entry_point": fields.get("entry_point", "course"),
                "pregnancy_term": fields.get("pregnancy_term"),
                "yoga_experience": fields.get("yoga_experience"),
                "contraindications": fields.get("contraindications"),
                "format": fields.get("format"),
                "contact": fields.get("contact"),
                "is_trial": fields.get("is_trial", False),
                "followup_stage": 0,
                "status": "new",
                "current_step": fields.get("current_step", "start"),
                "created_at": now()
            }
        }]
    }

    r = requests.post(_url("Applications"), headers=HEADERS, json=payload)
    r.raise_for_status()

    return r.json()


async def get_latest_application(user_id: int) -> dict | None:
    """
    Get the latest application for a user.
    """
    user = await get_grist_user(user_id)
    if not user:
        return None

    params = {
        "filter": json.dumps({"User": [user["id"]]})
    }

    r = requests.get(_url("Applications"), headers=HEADERS, params=params)
    r.raise_for_status()

    records = r.json().get("records", [])

    if not records:
        return None

    return max(records, key=lambda x: x["id"])


async def update_application(user_id: int, fields: dict) -> bool:
    """
    Update latest application for user.
    """
    app = await get_latest_application(user_id)
    if not app:
        return False

    payload = {
        "records": [{
            "id": app["id"],
            "fields": fields
        }]
    }

    r = requests.patch(_url("Applications"), headers=HEADERS, json=payload)
    r.raise_for_status()

    return True


async def get_applications(filter_status: str | None = None) -> list[dict]:
    """
    Get applications list (for admin panel).
    Optionally filter by status.
    """
    r = requests.get(_url("Applications"), headers=HEADERS)
    r.raise_for_status()

    records = r.json().get("records", [])
    result = []

    for rec in records:
        fields = rec["fields"]

        if filter_status and fields.get("status") != filter_status:
            continue

        result.append({
            "id": rec["id"],
            **fields
        })

    return result