from __future__ import annotations

from functools import lru_cache
from typing import Final, List

from core.settings import api_protect_settings

_IPS: Final[List[str]] = api_protect_settings.ALLOWED_IPS.split()


@lru_cache()
def is_allowed(host: str) -> bool:
    return host in _IPS
