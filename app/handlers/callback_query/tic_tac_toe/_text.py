from __future__ import annotations

from typing import Optional

from enums import Who
from schemas.tic_tac_toe import Player


def get_game_end_text(winner: Who, x_player: Player, o_player: Player) -> str:
    if winner == Who.X:
        text = f"{x_player.full_name} is winner!"
    elif winner == Who.O:
        text = f"{o_player.full_name} is winner!"
    else:
        text = "Is it really end!?"

    return text


def get_turn_text(current: Who, x_player: Player, o_player: Optional[Player] = None) -> str:
    if current == Who.X:
        text = f"{x_player.full_name} now your turn..."
    elif current == Who.O and o_player:
        text = f"{o_player.full_name} now your turn..."
    else:
        text = "Waiting for other player to join..."

    return text


def get_move_end_text(
    is_ended: bool, winner: Who, current: Who, x_player: Player, o_player: Optional[Player] = None
) -> str:
    return (
        get_game_end_text(winner=winner, x_player=x_player, o_player=o_player)
        if is_ended
        else get_turn_text(current=current, x_player=x_player, o_player=o_player)
    )
