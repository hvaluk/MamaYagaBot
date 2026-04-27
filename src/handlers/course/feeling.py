# src/handlers/course/feeling.py

from telebot.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from src.common import bot
from src.keyboards.inline_kb import build_inline_kb
from src.config import settings
from src.utils.state_manager import get_state, set_state, update_application, get_application
from src.utils.grist_helper import get_buttons_for_keyboard
from src.utils.humanize import FEELING_MAP
import json


def build_feeling_kb(selected: list[str], buttons: list[dict]):
    kb = InlineKeyboardMarkup()

    for btn in buttons:
        cb = btn["callback_data"]

        if cb == "feeling_done":
            continue

        label = btn["label"]
        prefix = "✅ " if label in selected else "⬜ "

        kb.add(InlineKeyboardButton(prefix + label, callback_data=cb))

    kb.add(InlineKeyboardButton("Готово", callback_data="feeling_done"))
    return kb


@bot.callback_query_handler(func=lambda c: c.data.startswith("feeling_") or c.data == "feeling_done")
async def course_feeling(call: CallbackQuery):

    user_id = call.from_user.id
    chat_id = call.message.chat.id

    state = await get_state(user_id)
    if state != "course_feeling":
        return

    await bot.answer_callback_query(call.id)

    app = await get_application(user_id)
    if not app:
        return

    raw = app["fields"].get("feelings")

    try:
        selected = json.loads(raw) if raw else []
    except:
        selected = []

    buttons = await get_buttons_for_keyboard("feeling_kb")

    # ---------------- TOGGLE ----------------
    if call.data != "feeling_done":

        value = FEELING_MAP.get(call.data)
        if not value:
            return

        if value in selected:
            selected.remove(value)
        else:
            selected.append(value)

        await update_application(user_id, {
            "feelings": json.dumps(selected, ensure_ascii=False)
        })

        kb = build_feeling_kb(selected, buttons)

        await bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=call.message.message_id,
            reply_markup=kb
        )
        return

    # ---------------- DONE ----------------
    if not selected:
        return await bot.send_message(chat_id, "Выбери хотя бы один вариант 💛")

    await set_state(user_id, "course_experience")

    kb = await build_inline_kb("experience_kb")

    await bot.send_message(
        chat_id,
        settings.get_text("ASK_EXPERIENCE"),
        reply_markup=kb
    )