# src/handlers/admin.py
from src.common import bot
from src.dao import crud
from src.config import ADMIN_IDS

def is_admin(user_id):
    return user_id in ADMIN_IDS

@bot.message_handler(commands=["requests"])
async def cmd_requests(message):
    if not is_admin(message.from_user.id):
        await bot.send_message(message.chat.id, "У вас нет доступа к этой команде.")
        return

    items = await crud.list_requests(limit=50)
    if not items:
        await bot.send_message(message.chat.id, "Нет заявок.")
        return

    texts = []
    for r in items:
        user = r.user
        name = user.first_name or (f"@{user.username}" if user.username else str(user.telegram_id))
        payload = r.payload or "-"
        texts.append(f"[{r.id}] {r.request_type} / {r.format_chosen or '-'} / {name} / {payload} / {r.created_at.isoformat()}")

    for i in range(0, len(texts), 20):
        chunk = "\n".join(texts[i:i+20])
        await bot.send_message(message.chat.id, f"Заявки:\n{chunk}")
