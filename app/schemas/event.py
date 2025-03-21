from __future__ import annotations

from typing import Any, Optional

from enums import EventType, Service

from .schema import ApplicationSchema


class Event(ApplicationSchema):
    service: Service
    type: EventType
    request: Optional[Any] = None
