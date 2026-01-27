# src/handlers/course/contra.py

from telebot.types import CallbackQuery
from src.common import bot
from src.dao.models import AsyncSessionLocal, Application
from src.keyboards.inline_kb import formats_kb, trial_lesson_kb
from src.keyboards.reply_kb import contact_request_kb
from src.texts.common import CONTRA_TEXT, FORMAT_TEXT, TRIAL_OFFER
from src.states import set_state, get_state, get_context, UserState


@bot.callback_query_handler(
    func=lambda c: c.data.startswith("contra_")
    and get_state(c.from_user.id) == UserState.COURSE_CONTRA
)
async def course_contra(call: CallbackQuery):
    await bot.answer_callback_query(call.id)

    user_id = call.from_user.id
    chat_id = call.message.chat.id
    value = call.data
    ctx = get_context(user_id)

    async with AsyncSessionLocal() as session:
        application = await session.get(Application, ctx["application_id"])
        application.contraindications = value

        if value == "contra_ok":
            application.current_step = "COURSE_FORMAT"
            set_state(user_id, UserState.COURSE_FORMAT)
        else:
            application.format = "contra"
            ctx["format"] = "contra"
            application.current_step = "COURSE_CONTACT"
            set_state(user_id, UserState.COURSE_CONTACT)

        await session.commit()

    if value == "contra_ok":
        if ctx.get("flow") == "trial":
            await bot.send_message(chat_id, TRIAL_OFFER, reply_markup=trial_lesson_kb())
        else:
            await bot.send_message(chat_id, FORMAT_TEXT, reply_markup=formats_kb())
    else:
        await bot.send_message(
            chat_id,
            f"{CONTRA_TEXT}\n\n"
            "Напиши, пожалуйста, свой Telegram или номер телефона для связи с Анной 💛",
            reply_markup=contact_request_kb(),
        )
