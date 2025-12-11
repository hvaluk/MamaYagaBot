# src/main.py

import asyncio
from src.common import bot
from src.handlers import *



if __name__ == "__main__":
   asyncio.run(bot.polling())
   
