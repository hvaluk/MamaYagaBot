# src/utils/broadcast.py

import asyncio
from datetime import datetime, timezone
import requests

from src.common import bot
from src.config import GRIST_BASE_URL, GRIST_DOC_ID, GRIST_API_KEY

HEADERS = {"Authorization": f"Bearer {GRIST_API_KEY}"}


# =========================================================
# TIME
# =========================================================

def utcnow():
    return datetime.now(timezone.utc)


def parse_dt(value):
    if not value:
        return None

    try:
        if isinstance(value, (int, float)):
            return datetime.fromtimestamp(value, tz=timezone.utc)

        if isinstance(value, str):
            return datetime.fromisoformat(value.replace("Z", "+00:00"))

    except Exception:
        return None

    return None


# =========================================================
# GET READY BROADCASTS
# =========================================================

async def get_pending_broadcasts():

    url = f"{GRIST_BASE_URL}{GRIST_DOC_ID}/tables/Broadcasts/records"

    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()

        records = r.json().get("records", [])
        now = utcnow()

        result = []

        for rec in records:

            f = rec.get("fields", {})

            if f.get("status") != "pending":
                continue

            scheduled = parse_dt(f.get("scheduled_at"))
            if not scheduled or scheduled > now:
                continue

            result.append(rec)

        return result

    except Exception as e:
        print(f"❌ get_pending_broadcasts error: {e}")
        return []


# =========================================================
# USERS
# =========================================================

async def get_target_users(target: str):

    url = f"{GRIST_BASE_URL}{GRIST_DOC_ID}/tables/Users/records"

    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()

        records = r.json().get("records", [])

        # ALL USERS
        if target == "all":
            return [
                str(r["fields"].get("TelegramID"))
                for r in records
                if r["fields"].get("TelegramID")
            ]

        # ACTIVE USERS (MANUAL is_active ONLY)
        if target == "active":
            return [
                str(r["fields"].get("TelegramID"))
                for r in records
                if r["fields"].get("TelegramID")
                and r["fields"].get("is_active") is True
            ]

        # CUSTOM IDS
        return [x.strip() for x in target.split(",") if x.strip()]

    except Exception as e:
        print(f"❌ get_target_users error: {e}")
        return []


# =========================================================
# STATUS UPDATE
# =========================================================

async def update_broadcast_status(row_id, status, sent_count=0):

    url = f"{GRIST_BASE_URL}{GRIST_DOC_ID}/tables/Broadcasts/records"

    payload = {
        "records": [{
            "id": row_id,
            "fields": {
                "status": status,
                "sent_count": sent_count
            }
        }]
    }

    try:
        requests.patch(url, headers=HEADERS, json=payload, timeout=10)
    except Exception as e:
        print(f"❌ update status error: {e}")


# =========================================================
# MAIN WORKER (SAFE + RESUME SUPPORT)
# =========================================================

async def broadcast_worker():

    print("📢 Broadcast worker started")

    while True:

        try:

            broadcasts = await get_pending_broadcasts()

            for bc in broadcasts:

                row_id = bc["id"]
                f = bc.get("fields", {})

                text = f.get("message_text")
                target = f.get("target")

                if not text or not target:
                    await update_broadcast_status(row_id, "failed")
                    continue

                users = await get_target_users(target)

                if not users:
                    await update_broadcast_status(row_id, "failed")
                    continue

                # mark as sending
                await update_broadcast_status(row_id, "sending")

                sent = 0
                failed = 0

                for tid in users:

                    try:
                        await bot.send_message(int(tid), text)
                        sent += 1
                        await asyncio.sleep(0.1)

                    except Exception as e:
                        failed += 1
                        print(f"❌ send failed {tid}: {e}")

                # FINAL STATE
                if failed == 0:
                    await update_broadcast_status(row_id, "sent", sent)
                else:
                    await update_broadcast_status(
                        row_id,
                        "sent_with_errors",
                        sent
                    )

                print(f"✅ Broadcast {row_id}: sent={sent}, failed={failed}")

        except Exception as e:
            print(f"❌ broadcast worker error: {e}")

        await asyncio.sleep(60)