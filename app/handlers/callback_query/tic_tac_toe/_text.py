from __future__ import annotations

from typing import Optional

from schemas import Player


def get_game_end_text(winner: Optional[Player]) -> str:
    if not winner:
        return "No winner today"
    return f"{winner.full_name} is winner!"


def get_turn_text(current: Optional[Player]) -> str:
    if not current:
        return "Well wait for other player"
    return f"{current.full_name} waiting for your move..."


def get_move_end_text(is_ended: bool, winner: Optional[Player], current: Optional[Player]) -> str:
    return get_game_end_text(winner=winner) if is_ended else get_turn_text(current=current)
