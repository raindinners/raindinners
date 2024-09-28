from __future__ import annotations

from typing import Any, Optional

from enums import EventType

from .schema import ApplicationSchema


class Event(ApplicationSchema):
    type: EventType
    request: Optional[Any] = None
