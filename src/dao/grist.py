import httpx
import os

GRIST_API_KEY = os.getenv("GRIST_API_KEY")
GRIST_DOC_ID = os.getenv("GRIST_DOC_ID")

BASE_URL = f"https://api.getgrist.com/api/docs/{GRIST_DOC_ID}/tables"


async def grist_create(table, data):
    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"{BASE_URL}/{table}/records",
            headers={"Authorization": f"Bearer {GRIST_API_KEY}"},
            json={"records": [{"fields": data}]}
        )
        return r.json()


async def grist_update(table, record_id, data):
    async with httpx.AsyncClient() as client:
        r = await client.patch(
            f"{BASE_URL}/{table}/records",
            headers={"Authorization": f"Bearer {GRIST_API_KEY}"},
            json={
                "records": [
                    {
                        "id": record_id,
                        "fields": data
                    }
                ]
            }
        )
        return r.json()


async def grist_get(table, record_id):
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{BASE_URL}/{table}/records/{record_id}",
            headers={"Authorization": f"Bearer {GRIST_API_KEY}"}
        )
        return r.json()


async def grist_list(table, filters=None):
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{BASE_URL}/{table}/records",
            headers={"Authorization": f"Bearer {GRIST_API_KEY}"}
        )
        data = r.json()["records"]

        if filters:
            data = [
                r for r in data
                if all(r["fields"].get(k) == v for k, v in filters.items())
            ]

        return data