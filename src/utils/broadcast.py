# src/utils/broadcast.py

import asyncio
from datetime import datetime, timezone
import requests

from src.common import bot
from src.config import GRIST_BASE_URL, GRIST_DOC_ID, GRIST_API_KEY, settings

HEADERS = {"Authorization": f"Bearer {GRIST_API_KEY}"}


async def get_pending_broadcasts() -> list[dict]:
    url = f"{GRIST_BASE_URL}{GRIST_DOC_ID}/tables/Broadcasts/records"
    
    try:
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(
            None,
            lambda: requests.get(url, headers=HEADERS, timeout=10)
        )
        r.raise_for_status()
        records = r.json().get("records", [])
        
        now = datetime.now(timezone.utc)
        pending = []
        
        for rec in records:
            f = rec.get("fields", {})
            if f.get("status") != "pending":
                continue
            
            scheduled = f.get("scheduled_at")
            if not scheduled:
                continue
        
            if isinstance(scheduled, (int, float)):
                scheduled_dt = datetime.fromtimestamp(scheduled, tz=timezone.utc)
            else:
                scheduled_dt = datetime.fromisoformat(str(scheduled).replace("Z", "+00:00"))
            
            if scheduled_dt <= now:
                pending.append(rec)
        
        return pending
        
    except Exception as e:
        print(f"❌ get_pending_broadcasts error: {e}")
        return []


async def get_target_users(target: str) -> list[str]:
    if target == "all":
        # All users
        url = f"{GRIST_BASE_URL}{GRIST_DOC_ID}/tables/Users/records"
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        records = r.json().get("records", [])
        return [str(rec["fields"].get("TelegramID")) for rec in records if rec["fields"].get("TelegramID")]
    
    elif target == "active":
        # Users with active status in Applications
        url = f"{GRIST_BASE_URL}{GRIST_DOC_ID}/tables/Applications/records"
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        records = r.json().get("records", [])
        
        user_ids = set()
        for rec in records:
            f = rec.get("fields", {})
            if f.get("status") not in ("done", "paid"):
                user_row = f.get("User")
                if user_row:
                    user_ids.add(user_row)

        # Receive Telegram IDs for these users
        result = []
        for user_row in user_ids:
            url = f"{GRIST_BASE_URL}{GRIST_DOC_ID}/tables/Users/records/{user_row}"
            r = requests.get(url, headers=HEADERS, timeout=10)
            if r.ok:
                tid = r.json().get("fields", {}).get("TelegramID")
                if tid:
                    result.append(str(tid))
        return result
    
    else:
        return [x.strip() for x in target.split(",") if x.strip()]


async def update_broadcast_status(row_id: int, status: str, sent_count: int = 0):
    url = f"{GRIST_BASE_URL}{GRIST_DOC_ID}/tables/Broadcasts/records"
    payload = {"records": [{"id": row_id, "fields": {
        "status": status,
        "sent_count": sent_count
    }}]}
    requests.patch(url, headers=HEADERS, json=payload, timeout=10)


async def broadcast_worker():
    print("📢 Broadcast worker started")
    
    while True:
        try:
            broadcasts = await get_pending_broadcasts()
            
            for bc in broadcasts:
                row_id = bc["id"]
                fields = bc.get("fields", {})
                
                text = fields.get("message_text", "")
                target = fields.get("target", "")
                
                if not text or not target:
                    await update_broadcast_status(row_id, "failed")
                    continue
                
                users = await get_target_users(target)
                sent = 0
                
                for tid in users:
                    try:
                        await bot.send_message(int(tid), text)
                        sent += 1
                        await asyncio.sleep(0.1)  # Throttling
                    except Exception as e:
                        print(f"❌ Broadcast to {tid} failed: {e}")
                
                await update_broadcast_status(row_id, "sent", sent)
                print(f"✅ Broadcast {row_id} sent to {sent} users")
        
        except Exception as e:
            print(f"❌ Broadcast worker error: {e}")
        
        await asyncio.sleep(60)
