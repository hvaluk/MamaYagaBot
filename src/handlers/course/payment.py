# src/handlers/course/payment.py

from telebot.types import CallbackQuery
from src.common import bot
from src.config import COURSE_PAY_LINK
from src.keyboards.inline_kb import payment_confirm_kb
from src.texts.common import PAYMENT_MESSAGE, PAYMENT_THANKS
from src.dao.models import AsyncSessionLocal, Application
from src.states import get_context, clear_state, set_context

# ---------------- Start payment ----------------
@bot.callback_query_handler(func=lambda c: c.data == "user:pay_course")
async def start_payment(callback: CallbackQuery):
    await bot.answer_callback_query(callback.id)

    user_id = callback.from_user.id
    ctx = get_context(user_id)
    application_id = ctx.get("application_id")

    async with AsyncSessionLocal() as session:
        if application_id:
            app = await session.get(Application, application_id)
        else:
            app = Application(
                user_id=user_id,
                entry_point=ctx.get("entry_point", "course"),
                format=ctx.get("selected_format", "Йога онлайн")
            )
            session.add(app)
            await session.commit()
            await session.refresh(app)
            set_context(user_id, application_id=app.id)

        # always stop follow-up
        app.followup_stage = 99
        app.followup_last_sent_at = None
        await session.commit()

    await bot.send_message(
        user_id,
        f"{PAYMENT_MESSAGE}\n\n👉 {COURSE_PAY_LINK}",
        reply_markup=payment_confirm_kb()
    )

# ---------------- Payment confirmation ----------------
@bot.callback_query_handler(func=lambda c: c.data == "user:paid")
async def confirm_payment(callback: CallbackQuery):
    await bot.answer_callback_query(callback.id)

    user_id = callback.from_user.id
    ctx = get_context(user_id)
    application_id = ctx.get("application_id")

    if not application_id:
        await bot.send_message(user_id, "Не вижу активную заявку 🙏")
        clear_state(user_id)
        return

    async with AsyncSessionLocal() as session:
        app = await session.get(Application, application_id)
        if not app:
            await bot.send_message(user_id, "Ошибка с заявкой 🙏")
            clear_state(user_id)
            return

        app.status = "paid_pending"  # awaiting admin confirmation
        app.current_step = "PAYMENT_CONFIRMED"
        app.followup_stage = 99
        if not app.format:
            app.format = ctx.get("selected_format", "Йога онлайн")
        await session.commit()

    await bot.send_message(user_id, PAYMENT_THANKS)
    clear_state(user_id)
