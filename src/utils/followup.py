# src/utils/followup.py

import asyncio
from datetime import datetime, timedelta
from sqlalchemy import select

from src.common import bot
from src.dao.models import AsyncSessionLocal, Application
from src.texts.common import FOLLOWUP_FIRST, FOLLOWUP_24H
from src.keyboards.inline_kb import followup_60min_kb, followup_24h_kb
from src.config import FOLLOWUP_CHECK_INTERVAL


def utcnow():
    return datetime.utcnow()


async def followup_worker():
    while True:
        async with AsyncSessionLocal() as session:
            now = utcnow()

            result = await session.execute(
                select(Application).where(
                    Application.is_trial.is_(True),
                    Application.followup_stage < 99,
                    Application.trial_opened_at.isnot(None)
                )
            )
            apps = result.scalars().all()

            for app in apps:
                if app.status in ("paid", "paid_pending"):
                    app.followup_stage = 99
                    continue

                delta = now - app.trial_opened_at
                last_sent = app.followup_last_sent_at or app.trial_opened_at

                # TEST: 1 минута
                if app.followup_stage == 0 and delta >= timedelta(minutes=1):
                    await bot.send_message(
                        app.user_id,
                        FOLLOWUP_FIRST,
                        reply_markup=followup_60min_kb()
                    )
                    app.followup_stage = 1
                    app.followup_last_sent_at = now

                # TEST: 2 минуты
                elif app.followup_stage == 1 and delta >= timedelta(minutes=2):
                    await bot.send_message(
                        app.user_id,
                        FOLLOWUP_24H,
                        reply_markup=followup_24h_kb()
                    )
                    app.followup_stage = 2
                    app.followup_last_sent_at = now

                # remind later
                elif app.followup_stage == 3:
                    if now - last_sent >= timedelta(minutes=3):
                        await bot.send_message(
                            app.user_id,
                            FOLLOWUP_24H,
                            reply_markup=followup_24h_kb()
                        )
                        app.followup_stage = 99

            await session.commit()

        await asyncio.sleep(FOLLOWUP_CHECK_INTERVAL)
