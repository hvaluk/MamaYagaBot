# src/utils/state_manager.py

from datetime import datetime, timezone

from src.utils.grist_helper import (
    get_latest_application,
    update_application,
)


# --------------------------- APPLICATION HELPERS ----------------------------

async def get_application(user_id: int) -> dict | None:
    """
    Возвращает последнюю заявку пользователя
    """
    return await get_latest_application(user_id)


async def get_applications(filter_status: str | None = None) -> list[dict]:
    """
    Возвращает список заявок (для админки)
    """
    from src.utils.grist_helper import get_applications as _get_apps
    return await _get_apps(filter_status)


# ---------------------------- STATE MANAGEMENT ------------------------------

async def set_state(user_id: int, state: str):
    """
    Устанавливает текущий шаг
    """
    await update_application(user_id, {
        "current_step": state
    })


async def get_state(user_id: int) -> str | None:
    """
    Получает текущий шаг
    """
    app = await get_application(user_id)
    if not app:
        return None

    return app["fields"].get("current_step")


async def update_application_data(user_id: int, fields: dict):
    """
    Обновляет данные заявки
    """
    return await update_application(user_id, fields)

update_application = update_application_data


# ------------------------------- CONTEXT -------------------------------

async def get_context(user_id: int) -> dict:
    """
    Если используешь context (JSON)
    """
    app = await get_application(user_id)
    if not app:
        return {}

    import json

    context = app["fields"].get("context")
    if not context:
        return {}

    try:
        return json.loads(context)
    except Exception:
        return {}


# ----------------------- FOLLOW-UP HELPERS ----------------------------    

async def stop_followup(user_id: int):
    """
    Остановить follow-up
    """
    await update_application(user_id, {
        "followup_stage": 99,
        "followup_last_sent_at": None
    })


async def mark_remind_later(user_id: int, days: int = 3):
    """
    Отложить follow-up
    """
    await update_application(user_id, {
        "followup_stage": days,
        "followup_last_sent_at": datetime.now(timezone.utc).isoformat()
    })