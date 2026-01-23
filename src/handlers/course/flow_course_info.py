# src/handlers/course/start.py

from telebot.types import CallbackQuery
from src.common import bot
from src.keyboards.inline_kb import course_flow_info_kb
from src.texts.course import ABOUT_PROGRAM
from src.states import set_context, set_state, UserState


@bot.callback_query_handler(func=lambda c: c.data == "flow_info")
async def start_course_flow(call: CallbackQuery):
    user_id = call.from_user.id

    # Сбрасываем флаг пробного потока
    set_context(user_id, trial_flow=False)

    await bot.send_message(call.message.chat.id, ABOUT_PROGRAM, reply_markup=course_flow_info_kb())
    set_state(user_id, UserState.COURSE_TERM)
