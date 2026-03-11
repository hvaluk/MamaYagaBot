# src/utils/followup.py

import asyncio
from datetime import datetime, timedelta, timezone
from sqlalchemy import select

from src.common import bot
from src.dao.models import AsyncSessionLocal, Application
from src.texts.common import FOLLOWUP_FIRST, FOLLOWUP_24H, FOLLOWUP_3D
from src.keyboards.inline_kb import (
    followup_60min_kb,
    followup_24h_kb,
    followup_3days_kb,
)
from src.config import get_setting


def utcnow():
    """Return current UTC time (timezone-aware)."""
    return datetime.now(timezone.utc)


def ensure_utc(dt: datetime | None) -> datetime | None:
    """
    Convert naive datetime from DB to UTC-aware datetime.
    SQLite often stores naive timestamps.
    """
    if dt is None:
        return None

    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)

    return dt


async def followup_worker():
    """Background worker for sending follow-up messages."""

    while True:
        try:
            async with AsyncSessionLocal() as session:
                now = utcnow()

                result = await session.execute(
                    select(Application).where(
                        Application.is_trial.is_(True),
                        Application.followup_stage < 99,
                        Application.trial_opened_at.isnot(None),
                    )
                )

                apps = result.scalars().all()

                for app in apps:
                    # Skip paid applications
                    if app.status in ("paid", "paid_pending"):
                        app.followup_stage = 99
                        continue

                    trial_time = ensure_utc(app.trial_opened_at)

                    if not trial_time:
                        continue

                    last_sent = ensure_utc(app.followup_last_sent_at) or trial_time

                    delta = now - trial_time

                    # 1️⃣ First follow-up after 60 minutes
                    if app.followup_stage == 0 and delta >= timedelta(minutes=60):
                        await bot.send_message(
                            app.user_id,
                            FOLLOWUP_FIRST,
                            reply_markup=followup_60min_kb(),
                        )

                        app.followup_stage = 1
                        app.followup_last_sent_at = now

                    # 2️⃣ Second follow-up after 24 hours
                    elif app.followup_stage == 1 and delta >= timedelta(hours=24):
                        await bot.send_message(
                            app.user_id,
                            FOLLOWUP_24H,
                            reply_markup=followup_24h_kb(),
                        )

                        app.followup_stage = 2
                        app.followup_last_sent_at = now

                    # 3️⃣ Remind later — 3 days after user requested
                    elif app.followup_stage == 3:
                        if now - last_sent >= timedelta(days=3):

                            name = ""
                            if app.user and app.user.first_name:
                                name = app.user.first_name

                            await bot.send_message(
                                app.user_id,
                                FOLLOWUP_3D.format(name=name),
                                reply_markup=followup_3days_kb(),
                            )

                            app.followup_stage = 99  # finalize

                await session.commit()

        except Exception as e:
            print(f"Followup worker error: {e}")

        interval = int(get_setting("FOLLOWUP_CHECK_INTERVAL", 60))
        await asyncio.sleep(interval)