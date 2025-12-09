# src/handlers/admin.py

from src.bot import bot
from src.config import ADMIN_IDS
from src.services.requests import list_requests  # предполагаем, что этот метод есть и асинхронный

def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

@bot.message_handler(commands=["requests"])
async def cmd_requests(message):
    if not is_admin(message.from_user.id):
        await bot.send_message(message.chat.id, "У вас нет доступа к этой команде.")
        return

    # Берем заявки через сервис requests.py
    items = await list_requests(limit=50)
    if not items:
        await bot.send_message(message.chat.id, "Нет заявок.")
        return

    texts = []
    for r in items:
        user = r.get('user', {})
        name = user.get('first_name') or (f"@{user.get('username')}" if user.get('username') else str(user.get('telegram_id')))
        payload = r.get('payload') or "-"
        texts.append(
            f"[{r.get('id')}] {r.get('request_type')} / {r.get('format_chosen') or '-'} / {name} / {payload} / {r.get('created_at')}"
        )

    # Отправляем по частям, чтобы Telegram не обрезал сообщения
    for i in range(0, len(texts), 20):
        chunk = "\n".join(texts[i:i+20])
        await bot.send_message(message.chat.id, f"Заявки:\n{chunk}")
