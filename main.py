# main.py

import asyncio
from src.common import bot
from src.handlers import *
from src.utils.followup import followup_worker


async def main():
    print("Bot is running...")
    # Запускаем воркер follow-up параллельно
    asyncio.create_task(followup_worker())
    try:
        await bot.infinity_polling(timeout=10, request_timeout=20)
    except Exception as e:
        print(f"ERROR in polling: {e}")
        await asyncio.sleep(5)
        await main()


if __name__ == "__main__":
    asyncio.run(main())
