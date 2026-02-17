# src/dao/models.py

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Text,
    ForeignKey,
    create_engine,
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

# --------------------Engines  --------------------

# async — for the bot
async_engine = create_async_engine(
    DATABASE_URL,
    echo=False,
)

AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# sync — for alembic
engine = create_engine(
    DATABASE_URL.replace("+aiosqlite", ""),
    future=True,
    echo=False,
)


def utcnow():
    """Naive UTC — единый стандарт"""
    return datetime.utcnow()


# --------------------  Models --------------------

class User(Base):
    __tablename__ = "users"

    telegram_id = Column(Integer, primary_key=True)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)

    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    registered_at = Column(DateTime, default=utcnow)

    applications = relationship(
        "Application",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    requests = relationship(
        "Request",
        back_populates="user",
        cascade="all, delete-orphan",
    )


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.telegram_id", ondelete="CASCADE"),
        nullable=False,
    )

    # where the user came from
    entry_point = Column(String, default="course")  # course | trial

    # questionnaire
    pregnancy_term = Column(String, nullable=True)
    yoga_experience = Column(String, nullable=True)
    contraindications = Column(String, nullable=True)
    format = Column(String, nullable=True)
    contact = Column(String, nullable=True)

    # trial
    is_trial = Column(Boolean, default=False)
    trial_opened_at = Column(DateTime, nullable=True)

    # follow-up
    followup_stage = Column(Integer, default=0)
    followup_last_sent_at = Column(DateTime, nullable=True)

    # оплата / статус
    status = Column(String, default="new")  # new | paid | paid_pending
    current_step = Column(String, default="COURSE_TERM")

    created_at = Column(DateTime, default=utcnow)

    user = relationship("User", back_populates="applications")


class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.telegram_id", ondelete="CASCADE"),
        nullable=False,
    )

    request_type = Column(String, nullable=False)  # question | callback | etc
    format_chosen = Column(String, nullable=True)
    payload = Column(Text, nullable=True)

    created_at = Column(DateTime, default=utcnow)

    user = relationship("User", back_populates="requests")
