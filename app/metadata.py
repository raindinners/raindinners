from __future__ import annotations

from typing import Final, Type, Union

from pokerengine.engine import EngineRake01

URANDOM_SIZE: Final[int] = 64
"""Using in function: `os.random` as `__size` argument."""

ENGINE_CLASS: Type[Union[EngineRake01]] = EngineRake01
"""Engine base class."""

START_TIME: Final[int] = 1
"""Start game after time (in seconds)."""

WINNERS_TIME: Final[int] = 10
"""How many time winners will be displaying (in seconds)."""

AUTO_ACTION_TIME: Final[int] = 10
"""Time to wait until player did a move (in seconds)."""

BALANCE_DEFAULT: Final[int] = 15000
"""Balance default amount. Warning: for emit changes run migrations."""

BONUS_AMOUNT: Final[int] = 10000
"""Bonus amount each player gets."""

BONUS_INCREMENT_TIME_HOURS: Final[int] = 4
"""Time, when next bonus can be got. Warning: for emit changes run migrations."""

RANDOM_MIN_VALUE: Final[int] = 0
"""Seed random min value."""

RANDOM_MAX_VALUE: Final[int] = 65535
"""Seed random max value"""

POOL_RECYCLE: Final[int] = 60 * 5
"""Value for recycle pool: 300 seconds."""

LOG_PER_REQUEST_LIMIT: Final[int] = 100
