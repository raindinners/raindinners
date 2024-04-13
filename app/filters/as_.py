from __future__ import annotations

from typing import Any, Dict, Generic, Optional, Type, TypeVar, Union

from aiogram.filters import Filter
from aiogram.types import TelegramObject
from pydantic import BaseModel, ValidationError
from redis.asyncio import Redis

from logger import logger

T = TypeVar("T", bound=BaseModel)


class As(Filter, Generic[T]):
    def __init__(
        self,
        as_: str,
        pydantic_class: Type[T],
        key: str = "inline_message_id",
        default: Optional[T] = None,
    ) -> None:
        self.as_ = as_
        self.pydantic_class = pydantic_class
        self.key = key
        self.default = default

    async def __call__(self, event: TelegramObject, redis: Redis) -> Union[bool, Dict[str, Any]]:
        value = await redis.get(name=getattr(event, self.key))

        try:
            return {self.as_: self.pydantic_class.model_validate_json(value)}
        except ValidationError as exc:
            if self.default:
                await redis.set(
                    name=getattr(event, self.key), value=self.default.model_dump_json()
                )
                return {self.as_: self.default}

            logger.exception(exc)

        return False
