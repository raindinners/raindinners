from __future__ import annotations

from typing import List, Optional

from distributed_websocket import Message, WebSocketManager
from pokerengine.enums import PositionE, RoundE
from pokerengine.pokerengine_core.engine import PlayerAction
from pokerengine.pokerengine_core.enums.action import ActionE

from enums import AutoEvent, Service
from logger import logger
from poker import Poker
from schemas import (
    Action,
    ApplicationResponse,
    ApplicationSchema,
    Card,
    Player,
    PokerCards,
    ToJSON,
    Traits,
)


class Information(ApplicationSchema):
    traits: Traits
    round: ToJSON[RoundE]
    players: List[Player]
    current: ToJSON[PositionE]
    poker_cards: PokerCards
    flop_dealt: bool
    pot: int
    pot_rake: int
    auto: Action
    time: Optional[float] = None
    actions: Optional[List[Action]] = None


def find_check_or_fold(actions: List[PlayerAction]) -> PlayerAction:
    for action in actions:
        if action.action == ActionE.CHECK:
            return action
        if action.action == ActionE.FOLD:
            return action

    return PlayerAction(amount=0, action=ActionE.NONE, position=PositionE.NONE)


def send_game_information(manager: WebSocketManager, poker: Poker) -> None:
    for position, player in enumerate(poker.engine.players.players):
        manager.send_by_conn_id(
            message=Message(
                data=ApplicationResponse[Information](
                    ok=True,
                    result=Information(
                        traits=Traits.model_validate(poker.engine.traits),
                        round=poker.engine.round.round,
                        flop_dealt=poker.engine.round.flop_dealt,
                        players=[
                            Player.model_validate(player)
                            for player in poker.engine.players.players
                        ],
                        current=poker.engine.positions.current,
                        poker_cards=PokerCards(
                            board=[
                                Card(value=card.card, string=str(card))
                                for card in poker.cards.board[
                                    : (
                                        poker.engine.round.round.value + 2
                                        if poker.engine.round.round != RoundE.PREFLOP
                                        else RoundE.PREFLOP.value
                                    )
                                ]
                            ],
                        ),
                        pot=poker.engine.pot.pot(),
                        pot_rake=poker.engine.pot.pot_rake(),
                        auto=Action.model_validate(
                            find_check_or_fold(actions=poker.engine.actions.actions)
                        ),
                        time=poker.auto_action_time,
                        actions=[
                            Action.model_validate(action)
                            for action in poker.engine.actions.actions
                        ],
                    ),
                    service=Service.POKER,
                    event_type=AutoEvent.INFORMATION,
                ).model_dump(),
                typ="json",
                conn_id=player.id,
            ),
        )


async def information(manager: WebSocketManager, poker: Poker) -> None:
    if not poker.started or poker.engine.round.terminal_state:
        return logger.debug("Skipping auto action: wrong game state")

    send_game_information(manager=manager, poker=poker)

    return None
