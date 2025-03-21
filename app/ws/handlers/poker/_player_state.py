from __future__ import annotations

from pokerengine.engine import Player as PPlayer

from orm import BalanceModel
from orm.core import sync_sessionmaker
from poker import Poker


def add_player(poker: Poker, stack: int, id_: str) -> None:
    poker.engine.players.add_player(stack=stack, id=id_)
    if not poker.started:
        poker.start_at = None


def remove_player(poker: Poker, player: PPlayer) -> None:
    poker.engine.players.remove_player(id=player.id)


def affect_player_joined_balance(stack: int, user_id: int) -> bool:
    with sync_sessionmaker.begin() as session:
        balance = BalanceModel.s_get_one_by(session, user_id=user_id)
        if balance.balance < stack:
            return False

        BalanceModel.s_update(
            session,
            values={BalanceModel.balance: BalanceModel.balance - stack},
            user_id=user_id,
        )

    return True


def affect_player_exited_balance(user_id: int, stack: int) -> None:
    with sync_sessionmaker.begin() as session:
        BalanceModel.s_update(
            session,
            values={BalanceModel.balance: BalanceModel.balance + stack},
            user_id=user_id,
        )
