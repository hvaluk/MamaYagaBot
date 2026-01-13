# main.py
import asyncio
from src.common import bot
from src.handlers import *

async def main():
    print("Bot is running...")
    try:
        await bot.infinity_polling(timeout=10, request_timeout=20)
    except Exception as e:
        print(f"ERROR in polling: {e}")
        await asyncio.sleep(5)
        await main()  # авто-restart при падении

if __name__ == "__main__":
    asyncio.run(main())
