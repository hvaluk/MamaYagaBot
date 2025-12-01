import asyncio
from src import handlers  # регистрирует все обработчики
from src.common import bot

if __name__ == "__main__":
    asyncio.run(bot.polling())