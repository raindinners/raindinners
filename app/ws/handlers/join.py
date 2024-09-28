from __future__ import annotations

from distributed_websocket import Connection, WebSocketManager
from redis.asyncio import Redis

from _redis import save
from schemas import Event
from utils.poker import get_poker
from ws.requests import JoinRequest

from ._messages import send_join_error, send_player_joined
from ._parser import update_event
from ._player_state import add_player, affect_player_joined_balance


async def join_handler(
    connection: Connection,
    manager: WebSocketManager,
    event: Event,
    redis: Redis,
) -> None:
    event = update_event(event=event, class_type=JoinRequest)
    poker = await get_poker(redis=redis, poker=event.request.poker)

    stack = poker.engine.traits.bb_bet * poker.engine.traits.bb_mult
    if not affect_player_joined_balance(stack=stack, user_id=int(connection.id)):
        send_join_error(connection=connection, manager=manager, event=event)
        return

    add_player(poker=poker, stack=stack, id_=connection.id)
    await save(redis=redis, key=event.request.poker, value=poker)

    send_player_joined(connection=connection, manager=manager, poker=poker, event=event)
