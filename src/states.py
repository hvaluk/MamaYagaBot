# src/states.py

from enum import Enum

class UserState(str, Enum):
    IDLE = "idle"
    COURSE_TERM = "course_term"
    COURSE_EXPERIENCE = "course_experience"
    COURSE_CONTRA = "course_contra"
    COURSE_FORMAT = "course_format"
    COURSE_PAY = "course_pay"      
    COURSE_CONTACT = "course_contact"

USER_STATES: dict[int, UserState] = {}

def set_state(user_id: int, state: UserState):
    if not isinstance(state, UserState):
        raise ValueError(f"Invalid state: {state}")
    USER_STATES[user_id] = state

def get_state(user_id: int) -> UserState | None:
    return USER_STATES.get(user_id)

def clear_state(user_id: int):
    USER_STATES.pop(user_id, None)
