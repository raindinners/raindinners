from __future__ import annotations

import datetime
from typing import Optional

from raindinners.types.base import RainDinnersObject


class Balance(RainDinnersObject):
    id: int
    """Balance ID in the system."""
    balance: int
    """Current balance for user."""
    bonus_time: Optional[datetime.datetime] = None
    """Time when the user got the bonus."""
