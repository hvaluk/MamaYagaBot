# src/services/requests.py
import aiohttp
import asyncio
from src.utils.airtable_client import AirtableClient
from src.config import FOLLOWUP_CHECK_INTERVAL
from src.bot import bot
from telebot import types
import logging

logger = logging.getLogger('followup')

class FollowupWorker:
    def __init__(self):
        self.interval = FOLLOWUP_CHECK_INTERVAL

    async def run(self):
        async with aiohttp.ClientSession() as sess:
            client = AirtableClient(sess)
            while True:
                try:
                    pending = await client.get_pending_followups()
                    for r in pending:
                        rec_id = r.get('id')
                        f = r.get('fields', {})
                        tid = f.get('TelegramID')
                        name = f.get('Name') or 'друг'
                        text = f'Привет, {name}! Как тебе первое занятие? Если есть вопросы — пиши, я на связи 🫶'
                        kb = types.InlineKeyboardMarkup()
                        kb.add(types.InlineKeyboardButton('Спасибо, занятие прошла', callback_data=f'follow_done_{rec_id}'))
                        kb.add(types.InlineKeyboardButton('Пока не успела', callback_data=f'follow_later_{rec_id}'))
                        try:
                            await bot.send_message(tid, text, reply_markup=kb)
                        except Exception:
                            logger.exception('send followup failed')
                        attempts = int(f.get('FollowupAttempts', 0) or 0) + 1
                        await client.update_request_fields(rec_id, {'FollowupAttempts': attempts})
                except Exception:
                    logger.exception('followup loop error')
                await asyncio.sleep(self.interval)
