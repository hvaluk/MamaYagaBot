# src/handlers/admin.py

from src.bot import bot
from src.config import ADMIN_IDS, AIRTABLE_BASE_ID, REQUESTS_TABLE
import aiohttp
from src.utils.airtable_client import AirtableClient

def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

async def list_requests(limit=50):
    async with aiohttp.ClientSession() as sess:
        client = AirtableClient(sess, f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}")
        records = await client.list_records(REQUESTS_TABLE, max_records=limit)
        result = []
        for r in records.get("records", []):
            fields = r.get("fields", {})
            result.append({
                "id": r.get("id"),
                "request_type": fields.get("Type"),
                "format_chosen": fields.get("Format"),
                "payload": fields.get("Payload"),
                "created_at": fields.get("CreatedAt"),
                "user": {
                    "telegram_id": fields.get("TelegramID"),
                    "first_name": fields.get("FirstName"),
                    "username": fields.get("Username"),
                }
            })
        return result

@bot.message_handler(commands=["requests"])
async def cmd_requests(message):
    if not is_admin(message.from_user.id):
        await bot.send_message(message.chat.id, "У вас нет доступа к этой команде.")
        return

    items = await list_requests(limit=50)
    if not items:
        await bot.send_message(message.chat.id, "Нет заявок.")
        return

    texts = []
    for r in items:
        user = r.get('user', {})
        name = user.get('first_name') or (f"@{user.get('username')}" if user.get('username') else str(user.get('telegram_id')))
        payload = r.get('payload') or "-"
        texts.append(f"[{r.get('id')}] {r.get('request_type')} / {r.get('format_chosen') or '-'} / {name} / {payload} / {r.get('created_at')}")

    # отправляем частями
    for i in range(0, len(texts), 20):
        chunk = "\n".join(texts[i:i+20])
        await bot.send_message(message.chat.id, f"Заявки:\n{chunk}")
