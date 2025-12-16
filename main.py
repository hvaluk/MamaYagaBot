# main.py

import asyncio
from src.common import bot
from src.handlers import *

async def main():
    print("Bot is running...")
    await bot.infinity_polling(timeout=10, request_timeout=20)

if __name__ == "__main__":
    asyncio.run(main())
