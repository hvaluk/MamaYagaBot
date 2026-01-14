# src/handlers/course/start.py
from telebot.types import CallbackQuery
from src.common import bot
from src.keyboards.inline_kb import pregnancy_kb
from src.texts.common import ASK_TERM
from src.states import set_state, UserState

@bot.callback_query_handler(func=lambda c: c.data == "start_course_flow")
async def start_course_flow(call: CallbackQuery):
    await bot.send_message(call.message.chat.id, ASK_TERM, reply_markup=pregnancy_kb())
    set_state(call.from_user.id, UserState.COURSE_TERM)
