# src/utils/followup.py

import asyncio
from src.common import bot
from src.dao.models import AsyncSessionLocal, Application
from src.keyboards.inline_kb import followup_60min_kb, followup_24h_kb
from src.texts.common import FOLLOWUP_FIRST, FOLLOWUP_24H


async def schedule_followup(user_id: int, application_id: int, step: int, delay_seconds: int):
    await asyncio.sleep(delay_seconds)

    async with AsyncSessionLocal() as session:
        application = await session.get(Application, application_id)

        if not application:
            return

        # 🛑 глобальные стоп-условия
        if application.status != "new":
            return

        if step == 1:
            if application.followup_1_sent:
                return

            await bot.send_message(
                user_id,
                FOLLOWUP_FIRST,
                reply_markup=followup_60min_kb()
            )
            application.followup_1_sent = True

        elif step == 2:
            if application.followup_2_sent:
                return

            await bot.send_message(
                user_id,
                FOLLOWUP_24H,
                reply_markup=followup_24h_kb()
            )
            application.followup_2_sent = True

        await session.commit()
