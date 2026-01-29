# src/dao/models.py

from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, Text, ForeignKey, create_engine
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from datetime import datetime
import os

Base = declarative_base()

DATABASE_URL = os.getenv(
    "MAMAYOGA_DATABASE_URL",
    "sqlite+aiosqlite:///mamayoga_bot.db"
)

# async
async_engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# sync (alembic)
engine = create_engine(
    DATABASE_URL.replace("+aiosqlite", ""),
    future=True
)


def utcnow():
    """Всегда naive UTC"""
    return datetime.utcnow()


class User(Base):
    __tablename__ = "users"

    telegram_id = Column(Integer, primary_key=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    registered_at = Column(DateTime, default=utcnow)

    applications = relationship("Application", back_populates="user")


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.telegram_id"), nullable=False)

    entry_point = Column(String, default="course")

    pregnancy_term = Column(String)
    yoga_experience = Column(String)
    contraindications = Column(String)
    format = Column(String)
    contact = Column(String)

    is_trial = Column(Boolean, default=False)
    trial_opened_at = Column(DateTime)              # NAIVE UTC

    followup_stage = Column(Integer, default=0)
    followup_last_sent_at = Column(DateTime)        # NAIVE UTC

    status = Column(String, default="new")
    current_step = Column(String, default="COURSE_TERM")

    created_at = Column(DateTime, default=utcnow)

    user = relationship("User", back_populates="applications")
