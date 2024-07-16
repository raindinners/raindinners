from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class RedisSupport(BaseModel):
    key: Optional[str] = None
