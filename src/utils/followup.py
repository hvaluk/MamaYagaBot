# src/utils/followup.py

import asyncio
from datetime import datetime, timedelta

from src.common import bot
from src.config import settings, MINSK_TZ
from src.keyboards.inline_kb import build_inline_kb

from src.utils.grist_helper import (
    get_followup_applications,
    get_telegram_id_by_user_row,
    update_application_by_row_id,
    get_grist_user_by_row_id,
)


# =========================================================
# TIME HELPERS
# =========================================================

def utcnow() -> datetime:
    return datetime.now(MINSK_TZ)


def parse_dt(value) -> datetime | None:

    if not value:
        return None

    try:

        if isinstance(value, (int, float)):
            return datetime.fromtimestamp(
                value,
                tz=MINSK_TZ,
            )

        if isinstance(value, str):

            dt = datetime.fromisoformat(
                value.replace("Z", "+00:00")
            )

            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=MINSK_TZ)
            else:
                dt = dt.astimezone(MINSK_TZ)

            return dt

    except Exception:
        return None

    return None


# =========================================================
# SEND FOLLOWUP MESSAGE
# =========================================================

async def send_followup_message(
    telegram_id: int | str,
    text: str,
    kb_name: str,
) -> bool:

    try:

        kb = await build_inline_kb(kb_name)

        await bot.send_message(
            chat_id=int(telegram_id),
            text=text,
            reply_markup=kb,
        )

        return True

    except Exception as e:

        print(
            f"[FOLLOWUP] send error [{telegram_id}]: {e}"
        )

        return False


# =========================================================
# FOLLOWUP WORKER
# =========================================================

async def followup_worker():

    print("[FOLLOWUP] worker started")

    while True:

        try:

            now = utcnow()

            applications = await get_followup_applications()

            for app in applications:

                try:

                    row_id = app.get("id")
                    fields = app.get("fields", {})

                    if not row_id:
                        continue

                    user_row_id = fields.get("User")

                    if not user_row_id:
                        continue

                    # =================================================
                    # STOP CONDITIONS
                    # =================================================

                    status = (
                        fields.get("status") or ""
                    ).lower()

                    if status in (
                        "done",
                        "paid",
                        "contact_requested",
                    ):
                        continue

                    # =================================================
                    # FOLLOWUP STAGE
                    # =================================================

                    stage = int(
                        fields.get("followup_stage") or 0
                    )

                    # =================================================
                    # TIME BASE
                    # =================================================

                    last_sent = parse_dt(
                        fields.get("followup_last_sent_at")
                    )

                    created_at = parse_dt(
                        fields.get("created_at")
                    )

                    base_time = last_sent or created_at

                    if not base_time:
                        continue

                    delta = now - base_time

                    # =================================================
                    # TELEGRAM ID
                    # =================================================

                    telegram_id = (
                        await get_telegram_id_by_user_row(
                            user_row_id
                        )
                    )

                    if not telegram_id:
                        continue

                    # =================================================
                    # USER DATA
                    # =================================================

                    user_data = (
                        await get_grist_user_by_row_id(
                            user_row_id
                        )
                    ) or {}

                    first_name = (
                        user_data.get("FirstName")
                        or ""
                    ).strip()

                    username = (
                        user_data.get("Username")
                        or ""
                    ).strip()

                    display_name = (
                        first_name or username
                    )

                    # =================================================
                    # STAGE 0 -> FIRST FOLLOWUP
                    # =================================================

                    if (
                        stage == 0
                        and delta >= timedelta(hours=24)
                    ):

                        text = settings.get_text(
                            "FOLLOWUP_FIRST"
                        )

                        success = await send_followup_message(
                            telegram_id=telegram_id,
                            text=text,
                            kb_name="followup_24h_kb",
                        )

                        if success:

                            await update_application_by_row_id(
                                row_id,
                                {
                                    "followup_stage": 1,
                                    "followup_last_sent_at": now.isoformat(),
                                },
                            )

                            print(
                                f"[FOLLOWUP] stage 0 -> 1 | {telegram_id}"
                            )

                    # =================================================
                    # STAGE 1 or 3 -> SECOND FOLLOWUP
                    # stage 3 = user clicked "remind later" from first followup
                    # =================================================

                    elif (
                        stage in (1, 3)
                        and delta >= timedelta(days=3)
                    ):

                        # ---------- GREETING ----------

                        if display_name:
                            greeting = f"Привет {display_name}\n\n"
                        else:
                            greeting = "Привет 💛\n\n"

                        # ---------- TEXT ----------

                        text = (
                            greeting
                            + settings.get_text("FOLLOWUP_3D")
                        )

                        # ---------- SEND ----------

                        success = await send_followup_message(
                            telegram_id=telegram_id,
                            text=text,
                            kb_name="followup_3days_kb",
                        )

                        # ---------- UPDATE ----------

                        if success:

                            await update_application_by_row_id(
                                row_id,
                                {
                                    "followup_stage": 99,
                                    "followup_last_sent_at": now.isoformat(),
                                },
                            )

                            print(
                                f"[FOLLOWUP] stage 1 -> done | {telegram_id}"
                            )

                except Exception as app_error:

                    print(
                        f"[FOLLOWUP] app error: {app_error}"
                    )

        except Exception as worker_error:

            print(
                f"[FOLLOWUP] worker error: {worker_error}"
            )

        await asyncio.sleep(
            settings.FOLLOWUP_CHECK_INTERVAL
        )