# utils/airtable_sync.py

import asyncio
from src.config import load_nocodb_settings, NOCODB_SETTINGS

NOCODB_REFRESH_INTERVAL = 300  # 5 минут

async def nocodb_worker():
    global NOCODB_SETTINGS

    while True:
        try:
            new_settings = load_nocodb_settings()

            if new_settings:
                NOCODB_SETTINGS.clear()
                NOCODB_SETTINGS.update(new_settings)
                print("NocoDB settings updated")

        except Exception as e:
            print(f"NocoDB sync error: {e}")

        await asyncio.sleep(NOCODB_REFRESH_INTERVAL)