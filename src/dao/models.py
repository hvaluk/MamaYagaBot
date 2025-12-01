import os
from sqlalchemy import Column, Integer, String, Boolean, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timezone

Base = declarative_base()

class User(Base):
    __tablename__ = 'MamaYogaBot_users'
    telegram_id = Column(Integer, primary_key=True)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    phone = Column(String(20), nullable=True)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    registered_at = Column(DateTime, default=datetime.now(timezone.utc))

# Синхронный движок для Alembic
engine = create_engine(
    os.getenv("MAMAYOGA_DATABASE_URL", "sqlite:///mamayoga_bot.db"),
    echo=True
)

# Асинхронный движок
DATABASE_URL = os.getenv("MAMAYOGA_DATABASE_URL", "sqlite+aiosqlite:///mamayoga_bot.db")
async_engine = create_async_engine(DATABASE_URL, echo=True)

# Асинхронная сессия
AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

