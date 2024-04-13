from __future__ import annotations

from typing import List

from pydantic import Field

from enums import TicTacToeColumn, TicTacToeRow, TicTacToeWho
from schemas._two_player_game import TwoPlayerGame


def _sum_row(map: List[List[TicTacToeWho]], row: TicTacToeRow) -> int:
    return sum((x.value for x in map[row.value]))


def _by_rows(map: List[List[TicTacToeWho]]) -> int:
    for row in TicTacToeRow:
        winner = _sum_row(map=map, row=row)
        if abs(winner) // 3 == 1:
            return winner // 3

    return TicTacToeWho.B.value


def _sum_column(map: List[List[TicTacToeWho]], column: TicTacToeColumn) -> int:
    return sum(row[column.value].value for row in map)


def _by_columns(map: List[List[TicTacToeWho]]) -> int:
    for column in TicTacToeColumn:
        winner = _sum_column(map=map, column=column)
        if abs(winner) // 3 == 1:
            return winner // 3

    return TicTacToeWho.B.value


def _sum_main_diagonal(map: List[List[TicTacToeWho]]) -> int:
    return sum(map[index][index].value for index in range(len(map)))


def _sum_secondary_diagonal(map: List[List[TicTacToeWho]]) -> int:
    return sum(map[index][len(map) - index - 1].value for index in range(len(map)))


def _by_diagonals(map: List[List[TicTacToeWho]]) -> int:
    winner = _sum_main_diagonal(map=map)
    if abs(winner) // 3 == 1:
        return winner // 3
    winner = _sum_secondary_diagonal(map=map)
    if abs(winner) // 3 == 1:
        return winner // 3

    return TicTacToeWho.B.value


def _is_draw(map: List[List[TicTacToeWho]]) -> bool:
    count = 0
    for row in map:
        for value in row:
            if value != TicTacToeWho.B:
                count += 1

    return count == len(TicTacToeRow) * len(TicTacToeColumn)


def _is_winner(map: List[List[TicTacToeWho]]) -> TicTacToeWho:
    return TicTacToeWho(_by_rows(map=map) or _by_columns(map=map) or _by_diagonals(map=map))


class TicTacToe(TwoPlayerGame):
    map: List[List[TicTacToeWho]] = Field(default_factory=list)
    turn: TicTacToeWho = TicTacToeWho.X
    is_ended: bool = False

    def move(self, row: TicTacToeRow, column: TicTacToeColumn) -> bool:
        if self.map[row.value][column.value] != TicTacToeWho.B or self.is_ended:
            return False

        self.map[row.value][column.value] = self.turn
        self.turn = TicTacToeWho.O if self.turn == TicTacToeWho.X else TicTacToeWho.X

        if _is_draw(map=self.map):
            self.is_ended = True

        if _is_winner(map=self.map) != TicTacToeWho.B:
            self.is_ended = True
            self.winner = self.current

        self.next_current()

        return True

    def reset(self) -> None:
        self.map = [
            [TicTacToeWho.B, TicTacToeWho.B, TicTacToeWho.B],
            [TicTacToeWho.B, TicTacToeWho.B, TicTacToeWho.B],
            [TicTacToeWho.B, TicTacToeWho.B, TicTacToeWho.B],
        ]
        self.switch_players()
        self.turn = TicTacToeWho.X
        self.is_ended = False
        self.winner = None
