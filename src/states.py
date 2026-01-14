# src/states.py
from enum import Enum

class UserState(str, Enum):
    IDLE = "idle"

    # COURSE FLOW
    COURSE_TERM = "course_term"
    COURSE_EXPERIENCE = "course_experience"
    COURSE_CONTRA = "course_contra"
    COURSE_FORMAT = "course_format"
    COURSE_CONTACT = "course_contact"

    # TRIAL FLOW
    TRIAL_TERM = "trial_term"
    TRIAL_EXPERIENCE = "trial_experience"
    TRIAL_CONTRA = "trial_contra"
    TRIAL_CONTENT = "trial_content"


USER_STATE: dict[int, UserState] = {}

def get_state(user_id: int) -> UserState:
    return USER_STATE.get(user_id, UserState.IDLE)

def set_state(user_id: int, state: UserState):
    USER_STATE[user_id] = state

def clear_state(user_id: int):
    USER_STATE.pop(user_id, None)
