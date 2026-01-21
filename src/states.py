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
USER_CONTEXT: dict[int, dict] = {}


def set_state(user_id: int, state: UserState):
    USER_STATES[user_id] = state


def get_state(user_id: int) -> UserState | None:
    return USER_STATES.get(user_id)


def clear_state(user_id: int):
    USER_STATES.pop(user_id, None)
    USER_CONTEXT.pop(user_id, None)


def set_context(user_id: int, **kwargs):
    USER_CONTEXT.setdefault(user_id, {}).update(kwargs)


def get_context(user_id: int) -> dict:
    return USER_CONTEXT.get(user_id, {})

