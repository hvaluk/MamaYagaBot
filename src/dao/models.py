import os
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import UTC, datetime
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'MamaYogaBot_users'

    telegram_id = Column(Integer, primary_key=True) # Telegram user ID
    username = Column(String, nullable=True) # Telegram username (can be null   if not set )
    first_name = Column(String, nullable=False) # User's first name
    last_name = Column(String, nullable=True) # User's last name (can be null if not set)
    phone = Column(String(20), nullable=True) # User's phone number (if provided)
    is_admin = Column(Boolean, default=False) # Is the user an admin
    is_active = Column(Boolean, default=True) # Is the user active
    registered_at = Column(DateTime, default=datetime.now(tz=UTC)) # Registration timestamp      

   
    def __repr__(self):
        return f"<User(id={self.telegram_id}, username='{self.username}')>"
    
engine = create_engine(
    os.getenv("MAMAYOGA_DATABASE_URL",
    'sqlite:///mamayoga_bot.db'), 
    echo=True)
