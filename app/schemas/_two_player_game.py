from __future__ import annotations

from typing import Optional

from .player import Player
from .redis import RedisSupport


class TwoPlayerGame(RedisSupport):
    first_player: Optional[Player] = None
    second_player: Optional[Player] = None
    current: Optional[Player] = None
    winner: Optional[Player] = None

    def add_player(self, player: Player) -> None:
        if not self.first_player:
            self.first_player = Player(
                user_id=player.user_id,
                full_name=player.full_name,
            )
            self.current = player

        if not self.second_player and self.first_player.user_id != player.user_id:
            self.second_player = Player(
                user_id=player.user_id,
                full_name=player.full_name,
            )
            self.current = player

    def next_current(self) -> None:
        self.current = (
            self.second_player
            if self.current and self.current.user_id == self.first_player.user_id
            else self.first_player
        )

    def switch_players(self) -> None:
        self.first_player, self.second_player = self.second_player, self.first_player
        self.current = self.first_player
        self.winner = None

    def in_game(self, player: Player) -> bool:
        return self.first_player == player or self.second_player == player

    def player_turn(self, player) -> bool:
        return self.current == player
