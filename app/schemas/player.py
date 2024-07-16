from __future__ import annotations

from pydantic import BaseModel


class Player(BaseModel):
    user_id: int
    full_name: str
