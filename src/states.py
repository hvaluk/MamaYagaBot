# src/states.py

from enum import Enum

class UserState(str, Enum):
    IDLE = "idle"
    WAITING_CONTACT = "waiting_contact"
    WAITING_TERM = "waiting_term"
    WAITING_EXPERIENCE = "waiting_experience"
    WAITING_CONTRA = "waiting_contra"
    WAITING_FORMAT = "waiting_format"

USER_STATE = {}

def get_state(user_id):
    return USER_STATE.get(user_id)

def set_state(user_id, state):
    USER_STATE[user_id] = state

def clear_state(user_id):
    USER_STATE.pop(user_id, None)
