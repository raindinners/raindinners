from __future__ import annotations

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from distributed_websocket import WebSocketManager
from fastapi.requests import Request
from fastapi.websockets import WebSocket
from redis.asyncio import Redis
from sqlalchemy.orm import Session

from orm.core import sync_sessionmaker


def get_sync_session() -> Session:  # type: ignore[misc]
    with sync_sessionmaker.begin() as session:
        yield session


def get_redis_from_request(request: Request) -> Redis:
    return request.app.state.redis


def get_redis(websocket: WebSocket) -> Redis:
    return websocket.app.state.redis


def get_websocket_manager_from_request(request: Request) -> WebSocketManager:
    return request.app.state.manager


def get_websocket_manager(websocket: WebSocket) -> WebSocketManager:
    return websocket.app.state.manager


def get_scheduler_from_request(request: Request) -> AsyncIOScheduler:
    return request.app.state.scheduler
