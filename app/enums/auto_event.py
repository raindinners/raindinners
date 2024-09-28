from __future__ import annotations

from enum import Enum


class AutoEvent(str, Enum):
    INFORMATION = "INFORMATION"
    START = "START"
    WINNERS = "WINNERS"
