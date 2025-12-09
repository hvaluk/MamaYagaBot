# src/services/requests.py

import asyncio
import logging
import aiohttp
from telebot import types
from src.utils.airtable_client import AirtableClient
from src.bot import bot
from src.config import AIRTABLE_BASE_ID, FOLLOWUP_CHECK_INTERVAL, REQUESTS_TABLE

logger = logging.getLogger('followup')


# -------------------------------
# Функция для создания заявки (для импорта в хендлеры)
# -------------------------------
async def create_request(telegram_id: int, request_type: str, format_chosen: str = None, payload: str = None, followup_hours: int = 24):
    async with aiohttp.ClientSession() as sess:
        client = AirtableClient(sess, f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}')
        return await client.create_request(
            telegram_id=telegram_id,
            request_type=request_type,
            format_chosen=format_chosen,
            payload=payload,
            followup_hours=followup_hours
        )


# -------------------------------
# Follow-up Worker для отправки сообщений
# -------------------------------
class FollowupWorker:
    def __init__(self, interval: int = FOLLOWUP_CHECK_INTERVAL):
        self.interval = interval

    async def run(self):
        async with aiohttp.ClientSession() as sess:
            client = AirtableClient(sess, f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}')
            while True:
                try:
                    pending = await client.get_pending_followups()
                    for r in pending:
                        rec_id = r['id']
                        f = r.get('fields', {})
                        tid = f.get('TelegramID')
                        name = f.get('Name') or 'друг'
                        text = (
                            f'Привет, {name}! Как тебе первое занятие? '
                            'Если есть вопросы — пиши, я на связи 🫶'
                        )
                        kb = types.InlineKeyboardMarkup()
                        kb.add(types.InlineKeyboardButton(
                            'Спасибо, занятие прошла',
                            callback_data=f'follow_done_{rec_id}'
                        ))
                        kb.add(types.InlineKeyboardButton(
                            'Пока не успела',
                            callback_data=f'follow_later_{rec_id}'
                        ))
                        try:
                            await bot.send_message(tid, text, reply_markup=kb)
                        except Exception:
                            logger.exception('send followup failed')

                        # Увеличиваем количество попыток follow-up
                        attempts = int(f.get('FollowupAttempts', 0) or 0) + 1
                        await client.update_record(REQUESTS_TABLE, rec_id, {'FollowupAttempts': attempts})

                except Exception:
                    logger.exception('followup loop error')

                await asyncio.sleep(self.interval)
