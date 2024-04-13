from __future__ import annotations

from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio.client import Redis

from core.middleware import create_middleware
from core.settings import fsm_settings
from handlers import setup_handlers


def create_dispatcher() -> Dispatcher:
    redis = Redis(host=fsm_settings.FSM_HOSTNAME, port=fsm_settings.FSM_PORT)

    dispatcher = Dispatcher(storage=RedisStorage(redis=redis), redis=redis)

    handlers_router = setup_handlers()
    dispatcher.include_router(handlers_router)

    create_middleware(dispatcher=dispatcher)

    return dispatcher
