# src/handlers/followup.py  

from src.bot import bot
from asyncio import sleep
from telebot.types import Message

async def send_followup(user_id: int, name: str):
    text = (
        f"Привет, {name}! Успела ли ты заметить, как изменилось твоё состояние? "
        "Часто после йоги появляется лёгкость, уходит напряжение с плеч и спины, "
        "а дыхание становится глубже и спокойнее.\n\n"
        "Если вдруг возникли вопросы по технике или хочешь узнать, как интегрировать практики в рутину — просто напиши мне.\n"
        "А если готова погрузиться глубже — напоминаю, что новогодняя цена на полный курс действует только до 31 декабря."
    )
    await sleep(3600)  # 60 минут
    await bot.send_message(user_id, text)
