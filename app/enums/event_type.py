from __future__ import annotations

from enum import Enum


class EventType(str, Enum):
    CREATE = "CREATE"
    EXECUTE_ACTION = "EXECUTE_ACTION"
    EXIT = "EXIT"
    GET_CARDS = "GET_CARDS"
    JOIN = "JOIN"
