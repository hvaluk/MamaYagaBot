import os
import asyncio
# from py_compile import main
from telebot.async_telebot import AsyncTeleBot
from dotenv import load_dotenv
from src import handlers  # Import handlers to register them

# Load variables from .env
load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")  

bot = AsyncTeleBot(TOKEN)




if __name__ == "__main__":
    asyncio.run(bot.polling())
