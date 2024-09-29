from __future__ import annotations

import time
from typing import List, Tuple, Union

from distributed_websocket import Message, WebSocketManager
from sqlalchemy.orm import Session

from enums import AutoEvent
from logger import logger
from metadata import WINNERS_TIME
from orm import BalanceModel
from orm.core import sync_sessionmaker
from poker import Poker
from schemas import ApplicationResponse
from utils.poker import get_entire_player_ids


def get_response(poker: Poker) -> Union[List[Tuple[str, int]], List[int]]:
    return (
        [(str(result), stack) for result, stack in poker.engine.pot.pay(cards=poker.cards)]
        if poker.engine.positions.showdown
        else poker.engine.pot.pay_noshowdown()
    )


def update_balances(
    session: Session,
    /,
    poker: Poker,
    response: Union[List[Tuple[str, int]], List[int]],
) -> None:
    for index, chips in enumerate(response):
        if isinstance(chips, Tuple):
            _, chips = chips

        player = poker.engine.players.players[index]
        BalanceModel.s_update(
            session,
            values={
                BalanceModel.balance: BalanceModel.balance + chips,
            },
            user_id=int(player.id),
        )


def send_winners(
    manager: WebSocketManager,
    poker: Poker,
    response: Union[List[Tuple[str, int]], List[int]],
) -> None:
    for index, chips in enumerate(response):
        if isinstance(chips, Tuple):
            result, chips = chips
        else:
            result, chips = "all exited", chips
        if chips > 0:
            result = "won by " + result
        else:
            result = "lose by " + result

        player = poker.engine.players.players[index]
        manager.send_by_conn_id(
            message=Message(
                data=ApplicationResponse[str](
                    ok=True,
                    result=f"Player #{player.id} got {chips} chips and {result}",
                    event_type=AutoEvent.LOG,
                ).model_dump(),
                typ="json",
                conn_id=get_entire_player_ids(poker=poker),
            )
        )

    manager.send_by_conn_id(
        message=Message(
            data=ApplicationResponse[Union[List[Tuple[str, int]], List[int]]](
                ok=True,
                result=response,
                event_type=AutoEvent.WINNERS,
            ).model_dump(),
            typ="json",
            conn_id=get_entire_player_ids(poker=poker),
        )
    )


async def winners(manager: WebSocketManager, poker: Poker) -> None:
    if not poker.started or not poker.engine.round.terminal_state:
        return logger.debug("Skipping winners: wrong state")

    response = get_response(poker=poker)
    with sync_sessionmaker.begin() as session:
        update_balances(session, poker=poker, response=response)

    send_winners(manager=manager, poker=poker, response=response)
    poker.started = False
    poker.winners_time = time.time() + WINNERS_TIME

    return None
