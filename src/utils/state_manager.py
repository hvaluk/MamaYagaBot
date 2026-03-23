# src/utils/state_manager.py

from datetime import datetime, timezone
import json
from src.utils.grist_helper import (
    get_latest_application,
    update_application as grist_update_application,
    get_applications as _get_apps,
)

# --------------------------- APPLICATION HELPERS ----------------------------
async def get_application(user_id: int) -> dict | None:
    return await get_latest_application(user_id)

async def get_applications(filter_status: str | None = None) -> list[dict]:
    return await _get_apps(filter_status)

# ---------------------------- STATE MANAGEMENT ------------------------------
async def set_state(user_id: int, state: str):
    await grist_update_application(user_id, {"current_step": state})

async def get_state(user_id: int) -> str | None:
    app = await get_application(user_id)
    if not app:
        return None
    return app["fields"].get("current_step")

async def update_application(user_id: int, fields: dict):
    return await grist_update_application(user_id, fields)

# ------------------------------- CONTEXT -------------------------------
async def get_context(user_id: int) -> dict:
    app = await get_application(user_id)
    if not app:
        return {}
    context = app["fields"].get("context")
    if not context:
        return {}
    try:
        return json.loads(context)
    except Exception:
        return {}

# ----------------------- FOLLOW-UP HELPERS ----------------------------
async def stop_followup(user_id: int):
    await grist_update_application(user_id, {"followup_stage": 99, "followup_last_sent_at": None})

async def mark_remind_later(user_id: int, days: int = 3):
    await grist_update_application(user_id, {
        "followup_stage": days,
        "followup_last_sent_at": datetime.now(timezone.utc).isoformat()
    })