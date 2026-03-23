# src/utils/followup.py

import asyncio
from datetime import datetime, timedelta, timezone
import requests

from src.common import bot
from src.config import settings, GRIST_BASE_URL, GRIST_DOC_ID, GRIST_API_KEY
from src.keyboards.inline_kb import build_inline_kb

HEADERS = {"Authorization": f"Bearer {GRIST_API_KEY}"}


# --- TIME HELPERS ---
def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def parse_iso(dt_str: str | None) -> datetime | None:
    if not dt_str:
        return None
    return datetime.fromisoformat(dt_str)


# --- GRIST HELPERS ---
def get_applications():
    """Fetch all active applications from Grist."""
    url = f"{GRIST_BASE_URL}{GRIST_DOC_ID}/tables/Applications/records"
    r = requests.get(url, headers=HEADERS, timeout=10)
    r.raise_for_status()
    return r.json().get("records", [])


def update_application(record_id: int, fields: dict):
    """Update application fields in Grist."""
    url = f"{GRIST_BASE_URL}{GRIST_DOC_ID}/tables/Applications/records"
    payload = {"records": [{"id": record_id, "fields": fields}]}
    requests.patch(url, headers=HEADERS, json=payload, timeout=10)


# --- WORKER ---
async def followup_worker():
    """
    Background worker that sends follow-up messages based on stage and elapsed time.
    Fully works via Grist.
    """
    while True:
        try:
            now = utcnow()
            records = get_applications()

            for rec in records:
                fields = rec.get("fields", {})

                user_id = fields.get("user_id")
                stage = fields.get("followup_stage", 0)
                status = fields.get("status")
                trial_time = parse_iso(fields.get("trial_opened_at"))
                last_sent = parse_iso(fields.get("followup_last_sent_at")) or trial_time

                if not user_id or not trial_time:
                    continue

                # Skip paid users
                if status in ("paid", "paid_pending"):
                    update_application(rec["id"], {"followup_stage": 99})
                    continue

                delta = now - trial_time

                # --- 60 MIN FOLLOW-UP ---
                if stage == 0 and delta >= timedelta(minutes=60):
                    kb = await build_inline_kb("followup_60min_kb")
                    text = settings.get_text("FOLLOWUP_FIRST")
                    await bot.send_message(user_id, text, reply_markup=kb)
                    update_application(rec["id"], {
                        "followup_stage": 1,
                        "followup_last_sent_at": now.isoformat()
                    })

                # --- 24H FOLLOW-UP ---
                elif stage == 1 and delta >= timedelta(hours=24):
                    kb = await build_inline_kb("followup_24h_kb")
                    text = settings.get_text("FOLLOWUP_24H")
                    await bot.send_message(user_id, text, reply_markup=kb)
                    update_application(rec["id"], {
                        "followup_stage": 2,
                        "followup_last_sent_at": now.isoformat()
                    })

                # --- 3 DAYS REMINDER ---
                elif stage == 3 and last_sent and (now - last_sent >= timedelta(days=3)):
                    kb = await build_inline_kb("followup_3days_kb")
                    text = settings.get_text("FOLLOWUP_3D", name="✨")
                    await bot.send_message(user_id, text, reply_markup=kb)
                    update_application(rec["id"], {
                        "followup_stage": 99
                    })

        except Exception as e:
            print(f"❌ Followup worker error: {e}")

        # Sleep before next check
        await asyncio.sleep(settings.FOLLOWUP_CHECK_INTERVAL)