# src/dao/models.py

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from datetime import datetime, timezone
import os

Base = declarative_base()

DATABASE_URL = os.getenv("MAMAYOGA_DATABASE_URL", "sqlite+aiosqlite:///mamayoga_bot.db")

# Асинхронный движок для бота
async_engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Синхронный движок для Alembic
engine = create_engine(
    DATABASE_URL.replace("+aiosqlite", ""),  # sqlite:///mamayoga_bot.db
    echo=True,
    future=True
)


class User(Base):
    __tablename__ = "users"

    telegram_id = Column(Integer, primary_key=True)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    registered_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    applications = relationship("Application", back_populates="user")
    requests = relationship("Request", back_populates="user")


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.telegram_id"), nullable=False)

    # entry point
    entry_point = Column(String, nullable=False, default="course")  # course | trial

    is_trial = Column(Boolean, default=False)

    # анкета
    pregnancy_term = Column(String, nullable=True)
    yoga_experience = Column(String, nullable=True)
    contraindications = Column(String, nullable=True)
    format = Column(String, nullable=True)
    contact = Column(String, nullable=True)

    # trial / follow-up
    trial_opened_at = Column(DateTime, nullable=True)
    followup_1_sent = Column(Boolean, default=False)
    followup_2_sent = Column(Boolean, default=False)

    # workflow
    status = Column(String, default="new")  # new | done | rejected
    current_step = Column(String, default="COURSE_TERM")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="applications")



class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.telegram_id"))
    request_type = Column(String, nullable=False)
    format_chosen = Column(String, nullable=True)
    payload = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="requests")
