# src/dao/crud.py
from .database import AsyncSessionLocal
from .models import User, Request, followup_after
from datetime import datetime
from sqlalchemy import select, update, insert, delete, desc

# USERS
async def get_user(telegram_id: int):
    async with AsyncSessionLocal() as s:
        return await s.get(User, telegram_id)

async def create_user(user_id: int, username: str = None, first_name: str = None, last_name: str = None, phone: str = None):
    async with AsyncSessionLocal() as s:
        user = User(
            telegram_id=user_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone=phone
        )
        s.add(user)
        await s.commit()
        await s.refresh(user)
        return user

async def upsert_user_contact(user_id: int, phone: str):
    async with AsyncSessionLocal() as s:
        user = await s.get(User, user_id)
        if not user:
            user = User(telegram_id=user_id, phone=phone)
            s.add(user)
        else:
            user.phone = phone
        await s.commit()
        await s.refresh(user)
        return user

# REQUESTS
async def create_request(user_id: int, request_type: str, format_chosen: str = None, payload: str = None, followup_hours: int = 24):
    async with AsyncSessionLocal() as s:
        r = Request(
            user_id=user_id,
            request_type=request_type,
            format_chosen=format_chosen,
            payload=payload,
            followup_at=followup_after(followup_hours)
        )
        s.add(r)
        await s.commit()
        await s.refresh(r)
        return r

async def get_pending_followups(max_attempts: int = 2):
    now = datetime.utcnow()
    async with AsyncSessionLocal() as s:
        q = select(Request).where(
            Request.is_followup_sent == False,
            Request.followup_at <= now,
            Request.followup_attempts < max_attempts
        )
        result = await s.execute(q)
        rows = result.scalars().all()
        # eager-load user relationship
        for r in rows:
            _ = r.user
        return rows

async def increment_followup_attempt(request_id: int):
    async with AsyncSessionLocal() as s:
        r = await s.get(Request, request_id)
        if r:
            r.followup_attempts = (r.followup_attempts or 0) + 1
            await s.commit()

async def mark_followup_sent(request_id: int):
    async with AsyncSessionLocal() as s:
        r = await s.get(Request, request_id)
        if r:
            r.is_followup_sent = True
            await s.commit()
            return True
        return False

async def list_requests(limit: int = 50):
    async with AsyncSessionLocal() as s:
        q = select(Request).order_by(desc(Request.created_at)).limit(limit)
        result = await s.execute(q)
        return result.scalars().all()
