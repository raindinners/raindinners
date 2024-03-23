from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel

from enums import Column, Row, Who

from .redis import RedisSupport


def _sum_row(map: List[List[Who]], row: Row) -> int:
    return sum((x.value for x in map[row.value]))


def _by_rows(map: List[List[Who]]) -> int:
    for row in Row:
        winner = _sum_row(map=map, row=row)
        if abs(winner) // 3 == 1:
            return winner // 3

    return Who.B.value


def _sum_column(map: List[List[Who]], column: Column) -> int:
    return sum(row[column.value].value for row in map)


def _by_columns(map: List[List[Who]]) -> int:
    for column in Column:
        winner = _sum_column(map=map, column=column)
        if abs(winner) // 3 == 1:
            return winner // 3

    return Who.B.value


def _sum_main_diagonal(map: List[List[Who]]) -> int:
    return sum(map[index][index].value for index in range(len(map)))


def _sum_secondary_diagonal(map: List[List[Who]]) -> int:
    return sum(map[index][len(map) - index - 1].value for index in range(len(map)))


def _by_diagonals(map: List[List[Who]]) -> int:
    winner = _sum_main_diagonal(map=map)
    if abs(winner) // 3 == 1:
        return winner // 3
    winner = _sum_secondary_diagonal(map=map)
    if abs(winner) // 3 == 1:
        return winner // 3

    return Who.B.value


def _is_draw(map: List[List[Who]]) -> bool:
    count = 0
    for row in map:
        for value in row:
            if value != Who.B:
                count += 1

    return count == len(Row) * len(Column)


def _is_winner(map: List[List[Who]]) -> Who:
    return Who(_by_rows(map=map) or _by_columns(map=map) or _by_diagonals(map=map))


class Player(BaseModel):
    user_id: int
    full_name: str


class TicTacToe(RedisSupport):
    map: List[List[Who]] = [
        [Who.B, Who.B, Who.B],
        [Who.B, Who.B, Who.B],
        [Who.B, Who.B, Who.B],
    ]
    x_player: Optional[Player] = None
    o_player: Optional[Player] = None
    current: Who = Who.X
    is_ended: bool = False
    winner: Who = Who.B

    def move(self, row: Row, column: Column) -> bool:
        if self.map[row.value][column.value] != Who.B or self.is_ended:
            return False

        self.map[row.value][column.value] = self.current
        self.current = Who.O if self.current == Who.X else Who.X

        if _is_draw(map=self.map):
            self.is_ended = True
        if (winner := _is_winner(map=self.map)) != Who.B:
            self.is_ended = True
            self.winner = winner

        return True

    def reset(self) -> None:
        self.map = [
            [Who.B, Who.B, Who.B],
            [Who.B, Who.B, Who.B],
            [Who.B, Who.B, Who.B],
        ]
        self.x_player, self.o_player = self.o_player, self.x_player
        self.current = Who.X
        self.is_ended = False
        self.winner = Who.B
