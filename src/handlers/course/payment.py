# src/handlers/course/payment.py

from telebot.types import CallbackQuery
from src.common import bot
from src.config import COURSE_PAY_LINK
from src.keyboards.inline_kb import payment_confirm_kb
from src.texts.common import PAYMENT_MESSAGE, PAYMENT_THANKS
from src.dao.models import AsyncSessionLocal, Application
from src.states import get_context, clear_state


@bot.callback_query_handler(func=lambda c: c.data == "pay_course")
async def start_payment(callback: CallbackQuery):
    await bot.answer_callback_query(callback.id)

    await bot.send_message(
        callback.from_user.id,
        f"{PAYMENT_MESSAGE}\n\n👉 {COURSE_PAY_LINK}",
        reply_markup=payment_confirm_kb()
    )

@bot.callback_query_handler(func=lambda c: c.data == "paid")
async def confirm_payment(callback: CallbackQuery):
    await bot.answer_callback_query(callback.id)

    user_id = callback.from_user.id
    ctx = get_context(user_id)
    application_id = ctx.get("application_id")

    if not application_id:
        await bot.send_message(
            user_id,
            "Я не нашла активную заявку 🙏 Давай начнём заново."
        )
        clear_state(user_id)
        return

    async with AsyncSessionLocal() as session:
        application = await session.get(Application, application_id)
        if application:
            application.status = "paid_pending"
            application.current_step = "PAYMENT_CONFIRMED"
            await session.commit()

    await bot.send_message(user_id, PAYMENT_THANKS)
    clear_state(user_id)

