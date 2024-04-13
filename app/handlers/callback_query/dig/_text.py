from __future__ import annotations

from typing import Optional

from schemas import Player


def get_game_end_text(winner: Player) -> str:
    return f"{winner.full_name} lucky-lucky (;"


def get_turn_text(current: Optional[Player]) -> str:
    if not current:
        return "Well wait for someone else with a shovel"
    return f"{current.full_name} go dig!"


def get_move_end_text(winner: Optional[Player], current: Optional[Player]) -> str:
    return get_game_end_text(winner=winner) if winner else get_turn_text(current=current)
