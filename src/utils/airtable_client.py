# src/utils/airtable_client.py

import aiohttp
import logging
from datetime import datetime, timezone, timedelta
from os import getenv
from dotenv import load_dotenv

load_dotenv()

AIRTABLE_API_KEY = getenv('AIRTABLE_API_KEY')
USERS_TABLE = getenv('AIRTABLE_USERS_TABLE', 'Users')
REQUESTS_TABLE = getenv('AIRTABLE_REQUESTS_TABLE', 'Requests')

logger = logging.getLogger(__name__)


class AirtableClient:
    def __init__(self, session: aiohttp.ClientSession, base_url: str):
        self.base_url = base_url
        self.session = session
        self.headers = {
            'Authorization': f'Bearer {AIRTABLE_API_KEY}',
            'Content-Type': 'application/json'
        }

    async def create_record(self, table: str, fields: dict):
        url = f'{self.base_url}/{table}'
        async with self.session.post(url, headers=self.headers, json={'fields': fields}) as r:
            text = await r.text()
            if r.status not in (200, 201):
                logger.error('create_record error %s %s', r.status, text)
                raise RuntimeError('Airtable create failed')
            return await r.json()

    async def update_record(self, table: str, record_id: str, fields: dict):
        url = f'{self.base_url}/{table}/{record_id}'
        async with self.session.patch(url, headers=self.headers, json={'fields': fields}) as r:
            text = await r.text()
            if r.status != 200:
                logger.error('update_record error %s %s', r.status, text)
                raise RuntimeError('Airtable update failed')
            return await r.json()

    async def list_records(self, table: str, max_records: int = 100):
        url = f'{self.base_url}/{table}'
        params = {'pageSize': max_records}
        async with self.session.get(url, headers=self.headers, params=params) as r:
            text = await r.text()
            if r.status != 200:
                logger.error('list_records error %s %s', r.status, text)
                raise RuntimeError('Airtable list failed')
            return await r.json()

    # --- Users ---
    async def get_user_by_telegram(self, telegram_id: int):
        res = await self.list_records(USERS_TABLE, max_records=100)
        for r in res.get('records', []):
            if r.get('fields', {}).get('TelegramID') == telegram_id:
                return r
        return None

    async def create_or_update_user(
        self, telegram_id: int, username=None, first_name=None, last_name=None, phone=None
    ):
        existing = await self.get_user_by_telegram(telegram_id)
        fields = {'TelegramID': telegram_id}
        if username: fields['Username'] = username
        if first_name: fields['FirstName'] = first_name
        if last_name: fields['LastName'] = last_name
        if phone: fields['Phone'] = phone

        if existing:
            return await self.update_record(USERS_TABLE, existing['id'], fields)
        else:
            return await self.create_record(USERS_TABLE, fields)

    # --- Requests ---
    async def create_request(
        self, telegram_id: int, request_type: str, format_chosen: str = None,
        payload: str = None, followup_hours: int = 24
    ):
        followup_at = (datetime.now(timezone.utc) + timedelta(hours=followup_hours)).isoformat()
        fields = {
            'TelegramID': telegram_id,
            'Type': request_type,
            'Format': format_chosen or '',
            'Payload': payload or '',
            'CreatedAt': datetime.now(timezone.utc).isoformat(),
            'FollowupAt': followup_at,
            'IsFollowupSent': False,
            'FollowupAttempts': 0,
        }
        return await self.create_record(REQUESTS_TABLE, fields)

    async def get_pending_followups(self, max_attempts: int = 2):
        res = await self.list_records(REQUESTS_TABLE, max_records=200)
        now = datetime.now(timezone.utc)
        pending = []
        for r in res.get('records', []):
            f = r.get('fields', {})
            try:
                if f.get('IsFollowupSent'): 
                    continue
                attempts = int(f.get('FollowupAttempts', 0) or 0)
                fa = f.get('FollowupAt')
                if not fa: 
                    continue
                fa_dt = datetime.fromisoformat(fa)
                if fa_dt <= now and attempts < max_attempts:
                    pending.append(r)
            except Exception as e:
                logger.error('Error processing record %s: %s', r, e)
        return pending
