# src/utils/state_manager.py

import json
from datetime import datetime, timezone

from src.utils.grist_helper import (
    get_latest_application,
    update_application as grist_update_application,
    get_applications as _get_apps,
)

DEFAULT_STATE = "idle"


# ===================== APPLICATION =====================

async def get_application(user_id: int) -> dict | None:
    return await get_latest_application(user_id)


async def get_applications(filter_status: str | None = None) -> list[dict]:
    return await _get_apps(filter_status)


async def update_application(user_id: int, fields: dict):
    return await grist_update_application(user_id, fields)


# ===================== STATE =====================

async def set_state(user_id: int, state: str):
    app = await get_application(user_id)

    if not app:
        print(f"⚠️ set_state: no application for user {user_id}")
        return False

    success = await grist_update_application(user_id, {
        "current_step": state
    })

    print(f"🧠 STATE SET [{user_id}] → {state}")

    return success


async def get_state(user_id: int) -> str:
    app = await get_application(user_id)

    if not app:
        return DEFAULT_STATE

    state = app["fields"].get("current_step")

    if not state:
        return DEFAULT_STATE

    return state


# ===================== CONTEXT =====================

async def get_context(user_id: int) -> dict:
    app = await get_application(user_id)

    if not app:
        return {}

    raw = app["fields"].get("context")

    if not raw:
        return {}

    try:
        return json.loads(raw)
    except Exception as e:
        print("❌ CONTEXT PARSE ERROR:", e)
        return {}


async def set_context(user_id: int, data: dict):
    await grist_update_application(user_id, {
        "context": json.dumps(data, ensure_ascii=False)
    })


# ===================== FOLLOW-UP =====================

async def stop_followup(user_id: int):
    await grist_update_application(user_id, {
        "followup_stage": 99,
        "followup_last_sent_at": None
    })


async def mark_remind_later(user_id: int, days: int = 3):
    await grist_update_application(user_id, {
        "followup_stage": days,
        "followup_last_sent_at": datetime.now(timezone.utc).isoformat()
    })