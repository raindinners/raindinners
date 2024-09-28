from __future__ import annotations

import random
import time
from typing import Optional

from distributed_websocket import Message, WebSocketManager
from pokerengine.constants import MAX_PLAYERS, MIN_PLAYERS

from enums import AutoEvent, State
from logger import logger
from metadata import RANDOM_MAX_VALUE, RANDOM_MIN_VALUE, START_TIME
from poker import Poker
from schemas import ApplicationResponse, ApplicationSchema
from utils.poker import get_entire_player_ids


class StartResponse(ApplicationSchema):
    state: State
    time: Optional[float] = None


def is_ready_to_start(poker: Poker) -> bool:
    players_to_save = [
        player for player in poker.engine.players.players if player.stack and not player.is_left
    ]
    poker.engine.players.set_players(players=players_to_save)

    return MIN_PLAYERS <= len(poker.engine.players.players) <= MAX_PLAYERS


def send_game_stopped(manager: WebSocketManager, poker: Poker) -> None:
    manager.send_by_conn_id(
        message=Message(
            data=ApplicationResponse[StartResponse](
                ok=True,
                result=StartResponse(state=State.STOPPED),
                event_type=AutoEvent.START,
            ).model_dump(),
            typ="json",
            conn_id=get_entire_player_ids(poker=poker),
        )
    )


def send_game_starting(manager: WebSocketManager, poker: Poker) -> None:
    manager.send_by_conn_id(
        message=Message(
            data=ApplicationResponse[StartResponse](
                ok=True,
                result=StartResponse(state=State.STARTING, time=poker.start_at),
                event_type=AutoEvent.START,
            ).model_dump(),
            typ="json",
            conn_id=get_entire_player_ids(poker=poker),
        )
    )


def send_game_started(manager: WebSocketManager, poker: Poker) -> None:
    manager.send_by_conn_id(
        message=Message(
            data=ApplicationResponse[StartResponse](
                ok=True,
                result=StartResponse(state=State.STARTED),
                event_type=AutoEvent.START,
            ).model_dump(),
            typ="json",
            conn_id=get_entire_player_ids(poker=poker),
        )
    )


async def remove_zero_balance_or_left_players(manager: WebSocketManager, poker: Poker) -> None:
    players_to_remove = {
        player.id for player in poker.engine.players.players if not player.stack or player.is_left
    }
    for connection in manager.active_connections:
        if connection.id in players_to_remove:
            await manager.close_connection(connection=connection)


async def start(manager: WebSocketManager, poker: Poker) -> None:
    if poker.started:
        await remove_zero_balance_or_left_players(manager=manager, poker=poker)

        return logger.debug("Skipping start: wrong state")

    if poker.winners_time and time.time() < poker.winners_time:
        return logger.debug("Skipping start: wrong state")

    if not is_ready_to_start(poker=poker):
        if poker.start_at or poker.winners_time:
            send_game_stopped(manager=manager, poker=poker)

        poker.stop()
        return logger.debug("Skipping start: wrong state")

    if not poker.start_at:
        poker.start_at = time.time() + START_TIME
        send_game_starting(manager=manager, poker=poker)

    if time.time() < poker.start_at:
        return logger.debug("Skipping start game: wrong time")

    poker.seed = random.randint(RANDOM_MIN_VALUE, RANDOM_MAX_VALUE)
    poker.start()
    send_game_started(manager=manager, poker=poker)

    return None
