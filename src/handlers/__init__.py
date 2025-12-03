# from src.handlers.welcome import send_welcome
# from src.handlers.rules import send_rules
# from src.handlers.message import echo_message


# __all__ = ["echo_message", "send_rules", "send_welcome"]

# src/handlers/__init__.py
# import handlers to register decorators on bot
from .welcome import *
from .menu import *
from .booking import *
from .admin import *
from .message import *
