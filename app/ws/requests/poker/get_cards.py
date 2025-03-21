from __future__ import annotations

from schemas import ApplicationSchema


class GetCardsRequest(ApplicationSchema):
    poker: str
