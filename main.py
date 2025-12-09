# main.py

import asyncio
from src.bot import bot, start_polling
from src.services.requests import FollowupWorker

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    worker = FollowupWorker()
    try:
        loop.create_task(worker.run())
        loop.run_until_complete(start_polling())
    except KeyboardInterrupt:
        print("Bot stopped")
