# src/handlers/course/trial.py

from telebot.types import CallbackQuery
from src.common import bot
from src.keyboards.inline_kb import pregnancy_kb
from src.texts.common import ASK_TERM
from src.states import set_context, set_state, UserState

@bot.callback_query_handler(func=lambda c: c.data == "flow_trial_start")
async def start_trial_flow(call: CallbackQuery):
    user_id = call.from_user.id

    # Сохраняем флаг пробного потока
    set_context(user_id, trial_flow=True)

    await bot.send_message(call.message.chat.id, ASK_TERM, reply_markup=pregnancy_kb())
    set_state(user_id, UserState.COURSE_TERM)
