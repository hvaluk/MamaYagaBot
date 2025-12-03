# src/main.py
import asyncio
import logging

from src.common import bot
import src.handlers  # registers handlers (side-effect imports)
from src.dao import crud, database
from src.config import FOLLOWUP_CHECK_INTERVAL
from telebot import types

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def followup_worker():
    while True:
        try:
            pending = await crud.get_pending_followups()
            for r in pending:
                try:
                    user = r.user
                    name = user.first_name or (f"@{user.username}" if user.username else "друг")
                    text = f"Привет, {name}! Как тебе первое занятие? Если есть вопросы — пиши, я на связи 🫶"
                    kb = types.InlineKeyboardMarkup()
                    kb.add(types.InlineKeyboardButton("Спасибо, занятие прошла", callback_data=f"follow_done_{r.id}"))
                    kb.add(types.InlineKeyboardButton("Пока не успела", callback_data=f"follow_later_{r.id}"))
                    try:
                        await bot.send_message(user.telegram_id, text, reply_markup=kb)
                    except Exception:
                        # user possibly blocked bot or can't be messaged
                        logger.exception("Failed to send followup message")
                    await crud.increment_followup_attempt(r.id)
                except Exception:
                    logger.exception("Error handling pending followup")
                    # ensure attempt increment to avoid infinite retry loop
                    try:
                        await crud.increment_followup_attempt(r.id)
                    except Exception:
                        pass
        except Exception:
            logger.exception("Error in followup_worker main loop")
        await asyncio.sleep(FOLLOWUP_CHECK_INTERVAL)

# callback handlers for followup replies are in handlers, but we need to react to callbacks:
@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("follow_done_"))
async def cb_follow_done(call):
    rid = int(call.data.split("_")[-1])
    await bot.answer_callback_query(call.id, "Отлично! Спасибо за фидбек.")
    await bot.send_message(call.message.chat.id, "Здорово! Продолжай в том же духе 💛")
    await crud.mark_followup_sent(rid)

@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("follow_later_"))
async def cb_follow_later(call):
    rid = int(call.data.split("_")[-1])
    await bot.answer_callback_query(call.id, "Хорошо, напомню позже.")
    # increment attempts on original, and create new request for +48 hours
    await crud.increment_followup_attempt(rid)
    await crud.create_request(call.from_user.id, "followup_retry", None, None, followup_hours=48)
    await bot.send_message(call.message.chat.id, "Окей — напомню позже.")

async def main():
    # ensure DB (create tables) — async
    await database.init_db()

    # start background followup worker
    asyncio.create_task(followup_worker())

    # start bot polling (async)
    await bot.polling(non_stop=True)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")
