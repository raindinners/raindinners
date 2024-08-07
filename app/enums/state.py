from __future__ import annotations

from ._enum import Enum


class State(Enum):
    """
    Represents player state in the game.
    """

    NONE = -1
    INIT = 0
    OUT = 1
    ALIVE = 2
    ALLIN = 3
