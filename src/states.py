# src/states.py
from enum import Enum

class UserState(str, Enum):
    IDLE = "idle"

    COURSE_TERM = "course_term"
    COURSE_EXPERIENCE = "course_experience"
    COURSE_CONTRA = "course_contra"
    COURSE_CONTACT = "course_contact"
    COURSE_FORMAT = "course_format"
    COURSE_PAY = "course_pay"

USER_STATE: dict[int, UserState] = {}

def get_state(user_id: int) -> UserState:
    return USER_STATE.get(user_id, UserState.IDLE)

def set_state(user_id: int, state: UserState):
    USER_STATE[user_id] = state

def clear_state(user_id: int):
    USER_STATE.pop(user_id, None)
