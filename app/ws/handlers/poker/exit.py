from __future__ import annotations

from distributed_websocket import Connection, WebSocketManager
from redis.asyncio import Redis

from _redis import save
from schemas import Event
from utils.poker import get_player_by_id, get_poker
from ws.requests import PokerExitRequest

from ._messages import send_player_left
from ._parser import update_event
from ._player_state import affect_player_exited_balance, remove_player


async def exit_handler(
    connection: Connection,
    manager: WebSocketManager,
    event: Event,
    redis: Redis,
) -> None:
    event = update_event(event=event, class_type=PokerExitRequest)
    poker = await get_poker(redis=redis, poker=event.request.poker)

    player = get_player_by_id(poker=poker, id_=connection.id)
    if not poker.started:
        affect_player_exited_balance(user_id=int(player.id), stack=player.stack)

    remove_player(poker=poker, player=player)
    await save(redis=redis, key=event.request.poker, value=poker)

    send_player_left(manager=manager, poker=poker, player=player, event=event)
