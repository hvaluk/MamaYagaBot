# src/handlers/course/back.py

from src.common import bot
from src.states import get_state, set_state, get_context, UserState
from src.keyboards.inline_kb import formats_kb, main_kb
from src.texts.common import FORMAT_TEXT
from src.texts.start import HELP_TEXT


async def handle_back(user_id: int, chat_id: int):
    state = get_state(user_id)
    ctx = get_context(user_id)

    flow = ctx.get("flow")
    fmt = ctx.get("format")

    # -------- TRIAL / INFO --------
    if flow in {"trial", "course_info"}:
        set_state(user_id, UserState.IDLE)
        await bot.send_message(chat_id, HELP_TEXT, reply_markup=main_kb())
        return

    # -------- CONTRA --------
    if fmt == "contra":
        set_state(user_id, UserState.IDLE)
        await bot.send_message(chat_id, HELP_TEXT, reply_markup=main_kb())
        return

    # -------- CONTACT --------
    if state == UserState.COURSE_CONTACT:
        set_state(user_id, UserState.COURSE_FORMAT)
        await bot.send_message(chat_id, FORMAT_TEXT, reply_markup=formats_kb())
        return

    # -------- PAY / FORMAT --------
    if state in {UserState.COURSE_PAY, UserState.COURSE_FORMAT}:
        set_state(user_id, UserState.COURSE_FORMAT)
        await bot.send_message(chat_id, FORMAT_TEXT, reply_markup=formats_kb())
        return

    # -------- FALLBACK --------
    set_state(user_id, UserState.IDLE)
    await bot.send_message(chat_id, HELP_TEXT, reply_markup=main_kb())
