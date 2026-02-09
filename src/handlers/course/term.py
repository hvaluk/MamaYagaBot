# src/handlers/course/term.py

from telebot.types import CallbackQuery
from src.common import bot
from src.dao.models import AsyncSessionLocal, Application
from src.keyboards.inline_kb import experience_kb
from src.texts.common import ASK_EXPERIENCE
from src.states import set_state, get_state, UserState, set_context

TERM_MAP = {
    "term_0_12": "до 12 недель",
    "term_12_29": "12–29 недель",
    "term_30_38": "30–38 недель",
    "term_38_plus": "38+ недель",
}

@bot.callback_query_handler(
    func=lambda c: c.data in TERM_MAP and get_state(c.from_user.id) == UserState.COURSE_TERM
)
async def course_term(call: CallbackQuery):
    await bot.answer_callback_query(call.id)
    term = TERM_MAP[call.data]
    user_id = call.from_user.id

    async with AsyncSessionLocal() as session:
        # Create a new Application
        application = Application(
            user_id=user_id,
            pregnancy_term=term,
            current_step="COURSE_EXPERIENCE"
        )
        session.add(application)
        await session.flush()  # obtain id for context
        await session.commit()

    # Save application_id in the user's context
    set_context(user_id, application_id=application.id)

    # Move to the next step — choose experience
    set_state(user_id, UserState.COURSE_EXPERIENCE)

    await bot.send_message(
        call.message.chat.id,
        ASK_EXPERIENCE,
        reply_markup=experience_kb()
    )
