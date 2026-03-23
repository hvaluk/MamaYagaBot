# main.py

import asyncio
import logging

from src.common import bot
from src.handlers import *  
from src.utils.followup import followup_worker
from src.config import config_updater_worker, settings


# --- LOGGING CONFIG ---

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)


# --- MAIN APP ---

async def main():
    logging.info("🚀 Bot is starting...")

    # --- Initial config load ---
    settings.refresh()

    # --- Background workers ---
    asyncio.create_task(config_updater_worker(settings.FOLLOWUP_CHECK_INTERVAL))
    asyncio.create_task(followup_worker())

    # --- Polling loop with auto-restart ---
    while True:
        try:
            logging.info("🤖 Bot polling started")
            await bot.infinity_polling(timeout=10, request_timeout=20)

        except Exception as e:
            logging.error(f"❌ Polling error: {e}", exc_info=True)

            # Prevent crash loop
            await asyncio.sleep(5)


# --- ENTRYPOINT ---

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("🛑 Bot stopped manually")