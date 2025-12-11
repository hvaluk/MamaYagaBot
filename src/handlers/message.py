# src/handlers/message.py

from src.common import bot

@bot.message_handler(func=lambda m: m.text and not m.text.startswith('/'))
async def echo_message(message):
    await bot.send_message(message.chat.id, "Спасибо! Чтобы выбрать действие — нажми /start")
