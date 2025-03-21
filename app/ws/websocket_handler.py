from __future__ import annotations

from distributed_websocket import Connection, WebSocketManager
from fastapi.websockets import WebSocketDisconnect
from redis.asyncio import Redis

from enums import EventType, Service
from exc import PlayerLeftError
from logger import logger
from schemas import Event

from .handlers import (
    poker_execute_action_handler,
    poker_exit_handler,
    poker_get_cards_handler,
    poker_join_handler,
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
            raise
        except Exception as exc:
            logger.exception(exc)


async def parse_event(
    connection: Connection, manager: WebSocketManager, event: Event, redis: Redis
) -> None:
    if event.service == Service.POKER:
        match event.type:
            case EventType.EXECUTE_ACTION:
                await poker_execute_action_handler(
                    connection=connection,
                    manager=manager,
                    event=event,
                    redis=redis,
                )
            case EventType.EXIT:
                await poker_exit_handler(
                    connection=connection,
                    manager=manager,
                    event=event,
                    redis=redis,
                )
            case EventType.GET_CARDS:
                await poker_get_cards_handler(
                    connection=connection,
                    manager=manager,
                    event=event,
                    redis=redis,
                )
            case EventType.JOIN:
                await poker_join_handler(
                    connection=connection,
                    manager=manager,
                    event=event,
                    redis=redis,
                )
    else:
        logger.debug("Got unresolved service")
