# src/handlers/course/payment.py

from telebot.types import CallbackQuery
from src.common import bot
from src.config import settings
from src.keyboards.reply_kb import build_inline_kb
from src.utils.state_manager import get_state, get_application, update_application, set_state


@bot.callback_query_handler(func=lambda c: c.data == "user:pay_course")
async def start_payment(callback: CallbackQuery):
    await bot.answer_callback_query(callback.id)
    user_id = callback.from_user.id

    app = await get_application(user_id)
    if not app:
        await bot.send_message(user_id, "Ошибка. Начни заявку заново")
        await set_state(user_id, "idle")
        return

    # --- STOP FOLLOW-UP ---
    await update_application(app["id"], {
        "followup_stage": 99,
        "followup_last_sent_at": None
    })

    # --- SEND PAYMENT LINK ---
    payment_kb = await build_inline_kb("payment_confirm_kb")
    payment_text = f"{settings.get_text('PAYMENT_MESSAGE')}\n\n{settings.COURSE_PAY_LINK}"
    await bot.send_message(user_id, payment_text, reply_markup=payment_kb)


@bot.callback_query_handler(func=lambda c: c.data == "user:paid")
async def confirm_payment(callback: CallbackQuery):
    await bot.answer_callback_query(callback.id)
    user_id = callback.from_user.id

    app = await get_application(user_id)
    if not app:
        await bot.send_message(user_id, "Не вижу активную заявку")
        await set_state(user_id, "idle")
        return

    # --- UPDATE APPLICATION ---
    await update_application(app["id"], {
        "status": "paid_pending",
        "current_step": "payment_confirmed",
        "followup_stage": 99
    })

    # --- CONFIRM TO USER ---
    await bot.send_message(user_id, settings.get_text("PAYMENT_THANKS"))
    await set_state(user_id, "idle")