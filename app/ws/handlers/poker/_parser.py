from __future__ import annotations

from typing import Type

from schemas import ApplicationSchema, Event


def update_event(event: Event, class_type: Type[ApplicationSchema]) -> Event:
    event.request = class_type.model_validate(event.request)
    return event
