from __future__ import annotations

from random import choices, randint
from typing import Final, List

from pydantic import Field

from enums import DigItem
from schemas._two_player_game import TwoPlayerGame

LEVEL_SIZE: Final[int] = 8
LEVELS: Final[int] = 8


class Dig(TwoPlayerGame):
    map: List[List[DigItem]] = Field(default_factory=list)
    diamond_position: List[int] = Field(default_factory=list)

    def move(self, row: int, index: int) -> bool:
        if self.winner:
            return False

        if self.map[row][index] == DigItem.USED:
            return False
        if row and self.map[row - 1][index] != DigItem.USED:
            return False
        if row and (
            self.map[row][max(index - 1, 0)] != DigItem.USED
            or self.map[row][min(index + 1, LEVEL_SIZE)] != DigItem.USED
        ):
            return False

        self.map[row][index] = DigItem.USED

        if self.diamond_position == [row, index]:
            self.winner = self.current
            self.map[row][index] = DigItem.DIAMOND

        self.next_current()

        return True

    def reset(self) -> None:
        self.map = [
            choices(
                list(DigItem),
                weights=[
                    LEVELS if not level else 0,
                    (LEVELS - level) // level if level else level,
                    level,
                    0,
                    0,
                ],
                k=LEVEL_SIZE,
            )
            for level in range(LEVELS)
        ]
        self.diamond_position = [randint(0, LEVELS), randint(0, LEVEL_SIZE)]
        self.switch_players()
        self.winner = None
