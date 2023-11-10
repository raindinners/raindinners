from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from raindinners.types.base import RainDinnersObject

if TYPE_CHECKING:
    from .balance import Balance


class User(RainDinnersObject):
    id: int
    """User ID in the system."""
    telegram_id: int
    """User Telegram ID."""
    username: Optional[str]
    """Optional. Username in the system."""
    photo_url: Optional[str]
    """Optional. User photo."""
    first_name: str
    """User first name."""
    last_name: Optional[str]
    """Optional. User second name."""
    full_name: str
    """User first and second names."""
    balance: Balance
    """User card games balance."""
