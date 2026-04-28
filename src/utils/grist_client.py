# src/utils/grist_client.py

import requests
from src.config import GRIST_BASE_URL, GRIST_DOC_ID, GRIST_API_KEY

HEADERS = {
    "Authorization": f"Bearer {GRIST_API_KEY}",
    "Content-Type": "application/json"
}


class GristClient:

    def __init__(self):
        self.base = f"{GRIST_BASE_URL}{GRIST_DOC_ID}/tables"

    def _url(self, table: str):
        return f"{self.base}/{table}/records"

    # ---------- BASIC METHODS ----------

    def fetch_all(self, table: str):
        try:
            r = requests.get(self._url(table), headers=HEADERS, timeout=10)
            r.raise_for_status()
            return r.json().get("records", [])
        except Exception as e:
            print(f"❌ GRIST FETCH ERROR [{table}]:", e)
            return []

    def insert(self, table: str, fields: dict):
        payload = {"records": [{"fields": fields}]}

        try:
            r = requests.post(self._url(table), headers=HEADERS, json=payload, timeout=10)

            print("GRIST RESPONSE:", r.status_code, r.text)

            r.raise_for_status()

            data = r.json()
            return data

        except Exception as e:
            print(f"❌ GRIST INSERT ERROR [{table}]:", repr(e))
            return None

    def update(self, table: str, record_id: int, fields: dict):
        payload = {"records": [{"id": record_id, "fields": fields}]}
        try:
            r = requests.patch(self._url(table), headers=HEADERS, json=payload, timeout=10)
            r.raise_for_status()
            return True
        except Exception as e:
            print(f"❌ GRIST UPDATE ERROR [{table}]:", e)
            return False


grist = GristClient()