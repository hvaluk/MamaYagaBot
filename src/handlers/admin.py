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
    if message.chat.type != "private":
        await bot.send_message(message.chat.id, "Команда доступна только в личных сообщениях.")
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
        created = r.created_at.strftime("%d.%m %H:%M")
        texts.append(f"[{r.id}] {r.request_type} / {r.format_chosen or '-'} / {name} / {payload} / {created}")

    for i in range(0, len(texts), 20):
        await bot.send_message(message.chat.id, "Заявки:\n" + "\n".join(texts[i:i+20]))
