from __future__ import annotations

from typing import Final, Type, Union

from pokerengine.engine import EngineRake01

ENGINE_CLASS: Type[Union[EngineRake01]] = EngineRake01
"""Engine base class."""

START_TIME: Final[int] = 5
"""Start game after time (in seconds)."""

WINNERS_TIME: Final[int] = 10
"""How many time winners will be displaying (in seconds)."""

AUTO_ACTION_TIME: Final[int] = 10
"""Time to wait until player did a move (in seconds)."""
