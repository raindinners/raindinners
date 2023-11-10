from __future__ import annotations

from raindinners.types.base import RainDinnersObject


class Authorization(RainDinnersObject):
    access_token: str
    """Token used in the system for authorization."""
