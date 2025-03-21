from __future__ import annotations

from distributed_websocket import Connection, WebSocketManager
from pokerengine.engine import PlayerAction
from pokerengine.enums import ActionE, PositionE
from redis.asyncio import Redis

from _redis import save
from schemas import Event
from utils.poker import get_poker
from ws.requests import PokerExecuteActionRequest

from ._messages import send_action_information, send_log
from ._parser import update_event


async def execute_action_handler(
    connection: Connection,
    manager: WebSocketManager,
    event: Event,
    redis: Redis,
) -> None:
    event = update_event(event=event, class_type=PokerExecuteActionRequest)
    poker = await get_poker(redis=redis, poker=event.request.poker)

    if (
        not poker.started
        or poker.engine.round.terminal_state
        or event.request.action.position != poker.engine.positions.current.value
    ):
        return send_action_information(
            connection=connection, manager=manager, event=event, executed=False
        )

    poker.execute(
        action=PlayerAction(
            action=ActionE(event.request.action.action),
            amount=event.request.action.amount,
            position=PositionE(event.request.action.position),
        )
    )
    await save(redis=redis, key=event.request.poker, value=poker)

    player = poker.engine.players.players[event.request.action.position]
    send_log(
        manager=manager,
        poker=poker,
        message=f"Player #{player.id} posted {ActionE(event.request.action.action).name.lower().capitalize()}",
    )
    send_action_information(connection=connection, manager=manager, event=event, executed=True)

    return None
