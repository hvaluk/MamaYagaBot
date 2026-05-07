# main.py

import asyncio
import logging

print("LOADING HANDLERS...")
import src.handlers
print("HANDLERS LOADED")

from src.common import bot
from src.utils.followup import followup_worker
from src.config import config_updater_worker, settings
from src.utils.broadcast import broadcast_worker


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)


async def start_background_tasks():
    settings.refresh()
    asyncio.create_task(
        config_updater_worker(settings.FOLLOWUP_CHECK_INTERVAL)
    )
    asyncio.create_task(
        followup_worker()
    )
    asyncio.create_task(
        broadcast_worker()
    )


async def main():
    logging.info("🚀 Bot is starting...")

    # start background tasks
    await start_background_tasks()

    logging.info("🤖 Bot polling started")

    await bot.infinity_polling(
        timeout=10,
        request_timeout=20,
        skip_pending=True
    )



if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("🛑 Bot stopped manually")