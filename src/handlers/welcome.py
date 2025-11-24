from main import bot

@bot.message_handler(commands=['start', 'help'])
async def send_welcome(message):
    text = 'Привет, я бот-помощник Анны. \n Я помогу тебе узнать о йоге для беременных и о клубе МамаМудра — женских практиках и восстановлении после родов.'
    await bot.reply_to(message, text)