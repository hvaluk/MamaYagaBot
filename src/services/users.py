# src/services/users.py

from src.utils.airtable_client import AirtableClient
import aiohttp

async def ensure_user(telegram_user):
    async with aiohttp.ClientSession() as sess:
        client = AirtableClient(sess)
        return await client.create_or_update_user(
            telegram_user.id,
            username=telegram_user.username,
            first_name=telegram_user.first_name,
            last_name=telegram_user.last_name
        )
