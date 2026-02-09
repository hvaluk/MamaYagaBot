
# src/handlers/course/contra.py

from telebot.types import CallbackQuery
from src.common import bot
from src.dao.models import AsyncSessionLocal, Application
from src.states import set_state, get_state, get_context, UserState

@bot.callback_query_handler(
    func=lambda c: c.data.startswith("contra_")
    and get_state(c.from_user.id) == UserState.COURSE_CONTRA
)
async def course_contra(call: CallbackQuery):
    await bot.answer_callback_query(call.id)
    user_id = call.from_user.id
    value = call.data
    ctx = get_context(user_id)
    trial_flow = ctx.get("trial_flow", False)

    async with AsyncSessionLocal() as session:
        application = await session.get(Application, ctx["application_id"])
        application.contraindications = value

        if value != "contra_ok":
            application.format = "contra"
            application.current_step = "COURSE_CONTACT"
            set_state(user_id, UserState.COURSE_CONTACT)
        else:
            application.current_step = "COURSE_FORMAT"
            set_state(user_id, UserState.COURSE_FORMAT)

        await session.commit()

    # ---------------- Sending messages ----------------
    if value == "contra_ok":
        if trial_flow:
            # Показываем пробный урок
            from src.keyboards.inline_kb import trial_lesson_kb
            from src.texts.common import TRIAL_OFFER

            await bot.send_message(
                call.message.chat.id,
                TRIAL_OFFER,
                reply_markup=trial_lesson_kb()
            )
        else:
            # Show course formats
            from src.keyboards.inline_kb import formats_kb
            from src.texts.common import FORMAT_TEXT

            await bot.send_message(
                call.message.chat.id,
                FORMAT_TEXT,
                reply_markup=formats_kb()
            )
    else:
        from src.keyboards.reply_kb import contact_request_kb
        from src.texts.common import CONTRA_TEXT

        await bot.send_message(
            call.message.chat.id,
            text= f"{CONTRA_TEXT}\n\nНапиши, пожалуйста, свой Telegram или номер телефона для связи с Анной 💛",
            reply_markup=contact_request_kb()
        )