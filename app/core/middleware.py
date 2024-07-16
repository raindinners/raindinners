from __future__ import annotations

from typing import Any, Awaitable, Callable, Dict, cast

from aiogram import BaseMiddleware, Dispatcher
from aiogram.types import TelegramObject
from redis.asyncio import Redis

from schemas import RedisSupport


class RedisValueAutoUpdateMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        value = await handler(event, data)
        if not isinstance(value, RedisSupport):
            return value

        redis = cast(Redis, data["redis"])
        await redis.set(name=value.key, value=value.model_dump_json())

        return value


def create_update_middleware(dispatcher: Dispatcher) -> None:
    dispatcher.update.middleware(RedisValueAutoUpdateMiddleware())


def create_middleware(dispatcher: Dispatcher) -> None:
    create_update_middleware(dispatcher=dispatcher)
