# src/dao/models.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta
from .database import Base

class User(Base):
    __tablename__ = "users"
    telegram_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    phone = Column(String(50), nullable=True)
    is_admin = Column(Boolean, default=False)
    registered_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class Request(Base):
    __tablename__ = "requests"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.telegram_id"), nullable=True)
    request_type = Column(String, nullable=False)   # "joined","payment","trial","booking"
    format_chosen = Column(String, nullable=True)   # "online","individual","consult"
    payload = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    followup_at = Column(DateTime, nullable=True)
    is_followup_sent = Column(Boolean, default=False)
    followup_attempts = Column(Integer, default=0)

    user = relationship("User", backref="requests")


def followup_after(hours: int = 24):
    return datetime.now(timezone.utc) + timedelta(hours=hours)
