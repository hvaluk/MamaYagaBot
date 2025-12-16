# src/states.py
from enum import Enum

class UserState(str, Enum):
    IDLE = "idle"
    WAITING_CONTACT = "waiting_contact"
