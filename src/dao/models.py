# src/dao/models.py
import os
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    telegram_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    phone = Column(String(50), nullable=True)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)   
    registered_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<User(telegram_id={self.telegram_id}, username={self.username})>"

engine = create_engine(
    os.getenv("MAMAYOGA_DATABASE_URL", "sqlite:///mamayoga_bot.db"), 
    echo=True
    )

async_engine = create_async_engine(
    os.getenv("MAMAYOGA_DATABASE_URL", "sqlite+aiosqlite:///mamayoga_bot.db"),
      echo=True
)

AsyncSessionLocal = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

# class Request(Base):
#     __tablename__ = "requests"
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.telegram_id"), nullable=True)
#     request_type = Column(String, nullable=False)   # "joined","payment","trial","booking"
#     format_chosen = Column(String, nullable=True)   # "online","individual","consult"
#     payload = Column(Text, nullable=True)
#     created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
#     followup_at = Column(DateTime, nullable=True)
#     is_followup_sent = Column(Boolean, default=False)
#     followup_attempts = Column(Integer, default=0)

#     user = relationship("User", backref="requests")


# def followup_after(hours: int = 24):
#     return datetime.now(timezone.utc) + timedelta(hours=hours)
