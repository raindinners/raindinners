from __future__ import annotations

from distributed_websocket import Connection, WebSocketManager
from redis.asyncio import Redis

from schemas import Card, Event, Hand, PlayerCards
from utils.poker import get_player_by_id, get_player_position, get_poker
from ws.requests import PokerGetCardsRequest

from ._messages import send_cards, send_cards_failed
from ._parser import update_event


async def get_cards_handler(
    connection: Connection,
    manager: WebSocketManager,
    event: Event,
    redis: Redis,
) -> None:
    event = update_event(event=event, class_type=PokerGetCardsRequest)
    poker = await get_poker(redis=redis, poker=event.request.poker)

    if not poker.started or poker.engine.round.terminal_state:
        return send_cards_failed(connection=connection, manager=manager, event=event)

    player = get_player_by_id(poker=poker, id_=connection.id)
    position = get_player_position(poker=poker, player=player)
    send_cards(
        connection=connection,
        manager=manager,
        cards=PlayerCards(
            hand=Hand(
                front=Card(
                    value=poker.cards.hands[position].value[0].card,
                    string=str(poker.cards.hands[position].value[0]),
                ),
                back=Card(
                    value=poker.cards.hands[position].value[1].card,
                    string=str(poker.cards.hands[position].value[1]),
                ),
            ),
        ),
        player=player,
        event=event,
    )

    return None
