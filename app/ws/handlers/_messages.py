from __future__ import annotations

from distributed_websocket import Connection, Message, WebSocketManager
from pokerengine.engine import Player as PPlayer

from enums import AutoEvent
from poker import Poker
from schemas import ApplicationResponse, Event, Player, PlayerCards
from utils.poker import get_entire_player_ids, get_player_by_id


def send_log(
    manager: WebSocketManager,
    poker: Poker,
    message: str,
) -> None:
    manager.send_by_conn_id(
        message=Message(
            data=ApplicationResponse[str](
                ok=True,
                result=message,
                event_type=AutoEvent.LOG,
            ).model_dump(),
            typ="json",
            conn_id=get_entire_player_ids(poker=poker),
        )
    )


def send_cards(
    connection: Connection,
    manager: WebSocketManager,
    cards: PlayerCards,
    player: Player,
    event: Event,
) -> None:
    manager.send_by_conn_id(
        message=Message(
            data=ApplicationResponse[PlayerCards](
                ok=True, result=cards, player=player, event_type=event.type
            ).model_dump(),
            typ="json",
            conn_id=connection.id,
        ),
    )


def send_cards_failed(connection: Connection, manager: WebSocketManager, event: Event) -> None:
    manager.send_by_conn_id(
        message=Message(
            data=ApplicationResponse[bool](
                ok=False, result=False, event_type=event.type
            ).model_dump(),
            typ="json",
            conn_id=connection.id,
        ),
    )


def send_action_information(
    connection: Connection, manager: WebSocketManager, event: Event, executed: bool
) -> None:
    manager.send_by_conn_id(
        message=Message(
            data=ApplicationResponse[bool](
                ok=True,
                result=executed,
                event_type=event.type,
            ).model_dump(),
            typ="json",
            conn_id=connection.id,
        ),
    )


def send_player_joined(
    connection: Connection, manager: WebSocketManager, poker: Poker, event: Event
) -> None:
    manager.send_by_conn_id(
        message=Message(
            data=ApplicationResponse[Player](
                ok=True,
                result=Player.model_validate(get_player_by_id(poker=poker, id_=connection.id)),
                event_type=event.type,
            ).model_dump(),
            typ="json",
            conn_id=get_entire_player_ids(poker=poker),
        )
    )


def send_join_error(connection: Connection, manager: WebSocketManager, event: Event) -> None:
    manager.send_by_conn_id(
        message=Message(
            data=ApplicationResponse[bool](
                ok=False,
                result=False,
                event_type=event.type,
            ).model_dump(),
            typ="json",
            conn_id=connection.id,
        )
    )


def send_player_left(
    manager: WebSocketManager, poker: Poker, player: PPlayer, event: Event
) -> None:
    manager.send_by_conn_id(
        message=Message(
            data=ApplicationResponse[Player](
                ok=True,
                result=Player.model_validate(player),
                event_type=event.type,
            ).model_dump(),
            typ="json",
            conn_id=get_entire_player_ids(poker=poker),
        )
    )
