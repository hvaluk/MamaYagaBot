# src/dao/crud.py
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.dao.models import AsyncSessionLocal, User, Request

async def list_requests(limit: int = 50):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User)
            .options(selectinload(User.requests))
            .order_by(User.registered_at.desc())
            .limit(limit)
        )
        return result.scalars().all()
