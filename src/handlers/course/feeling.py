# src/handlers/course/feeling.py

from telebot.types import CallbackQuery
from src.common import bot
from src.keyboards.inline_kb import build_inline_kb
from src.config import settings
from src.utils.state_manager import get_state, set_state, update_application, get_application
from src.utils.humanize import FEELING_MAP
import json
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def build_feeling_kb(selected: list[str]):
    kb = InlineKeyboardMarkup()

    for key, text in FEELING_MAP.items():
        # Add visual indicator for selected/unselected items
        prefix = "✅ " if text in selected else "⬜ "
        kb.add(InlineKeyboardButton(
            prefix + text,
            callback_data=key
        ))

    # Add confirmation button
    kb.add(InlineKeyboardButton("Готово", callback_data="feeling_done"))
    return kb


@bot.callback_query_handler(func=lambda c: c.data in FEELING_MAP or c.data == "feeling_done")
async def course_feeling(call: CallbackQuery):
    user_id = call.from_user.id

    # --- STATE CHECK ---
    # Ensure user is on the correct step
    state = await get_state(user_id)
    if state != "course_feeling":
        return

    # Acknowledge callback to remove loading state in Telegram
    await bot.answer_callback_query(call.id)

    # --- LOAD CURRENT FEELINGS FROM DB ---
    app = await get_application(user_id)
    current = app["fields"].get("feelings")

    try:
        # Parse stored JSON list
        feelings = json.loads(current) if current else []
    except:
        feelings = []

    # --- HANDLE OPTION CLICK ---
    if call.data in FEELING_MAP:
        value = FEELING_MAP[call.data]

        # Toggle selection (add/remove)
        if value in feelings:
            feelings.remove(value)
        else:
            feelings.append(value)

        # Save updated list to DB
        await update_application(user_id, {
            "feelings": json.dumps(feelings, ensure_ascii=False)
        })

        # --- UPDATE KEYBOARD UI ---
        # Rebuild keyboard with updated selection state
        kb = build_feeling_kb(feelings)

        # Update existing message instead of sending new one
        await bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=kb
        )
        return

    # --- HANDLE "DONE" BUTTON ---
    if call.data == "feeling_done":
        # Move user to next step
        await update_application(user_id, {
            "current_step": "course_experience"
        })

        await set_state(user_id, "course_experience")

        # Send next question
        kb = await build_inline_kb("experience_kb")

        await bot.send_message(
            call.message.chat.id,
            settings.get_text("ASK_EXPERIENCE"),
            reply_markup=kb
        )