from __future__ import annotations

from distributed_websocket import Connection, WebSocketManager
from fastapi.websockets import WebSocketDisconnect
from redis.asyncio import Redis

from enums import EventType
from exc import PlayerLeftError
from logger import logger
from schemas import Event

from .handlers import (
    execute_action_handler,
    exit_handler,
    get_cards_handler,
    join_handler,
)


async def websocket_handler(
    connection: Connection, manager: WebSocketManager, redis: Redis
) -> None:
    while True:
        event = Event.model_validate(await connection.receive_json())

        logger.info(event)
        try:
            await parse_event(
                connection=connection,
                manager=manager,
                event=event,
                redis=redis,
            )
        except (WebSocketDisconnect, PlayerLeftError):
            logger.debug("Player left")
            return
        except Exception as exc:
            logger.exception(exc)


async def parse_event(
    connection: Connection, manager: WebSocketManager, event: Event, redis: Redis
) -> None:
    match event.type:
        case EventType.EXECUTE_ACTION:
            await execute_action_handler(
                connection=connection,
                manager=manager,
                event=event,
                redis=redis,
            )
        case EventType.EXIT:
            await exit_handler(
                connection=connection,
                manager=manager,
                event=event,
                redis=redis,
            )
        case EventType.GET_CARDS:
            await get_cards_handler(
                connection=connection,
                manager=manager,
                event=event,
                redis=redis,
            )
        case EventType.JOIN:
            await join_handler(
                connection=connection,
                manager=manager,
                event=event,
                redis=redis,
            )
