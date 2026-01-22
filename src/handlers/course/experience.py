# src/handlers/course/experience.py

from telebot.types import CallbackQuery
from src.common import bot
from src.dao.models import AsyncSessionLocal, Application
from src.keyboards.inline_kb import contra_kb
from src.texts.common import SAFE_TEXT_EXPERIENCED, SAFE_TEXT
from src.states import set_state, get_state, get_context, UserState

EXP_MAP = {
    "exp_none": "нет",
    "exp_some": "немного",
    "exp_regular": "регулярно",
}

@bot.callback_query_handler(
    func=lambda c: c.data in EXP_MAP
    and get_state(c.from_user.id) == UserState.COURSE_EXPERIENCE
)
async def course_experience(call: CallbackQuery):
    await bot.answer_callback_query(call.id)
    user_id = call.from_user.id
    value = EXP_MAP[call.data]  
    ctx = get_context(user_id)

    async with AsyncSessionLocal() as session:
        application = await session.get(Application, ctx["application_id"])
        application.yoga_experience = value
        application.current_step = "COURSE_CONTRA"
        await session.commit()

    set_state(user_id, UserState.COURSE_CONTRA)

 
    if value in ["нет", "немного"]:
        await bot.send_message(
            call.message.chat.id,
            SAFE_TEXT,
            reply_markup=contra_kb()
        )
    elif value == "регулярно":
        await bot.send_message(
            call.message.chat.id,
            SAFE_TEXT_EXPERIENCED,
            reply_markup=contra_kb()
        )
