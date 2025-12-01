from src.common import bot

@bot.message_handler(commands=['start', 'help'])
async def send_welcome(message):
    text = 'Привет, я бот-помощник Анны. \nЯ помогу тебе узнать о йоге для беременных.'
    await bot.reply_to(message, text)