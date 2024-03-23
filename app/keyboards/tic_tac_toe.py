from __future__ import annotations

from typing import List

from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback_data import TicTacToeMoveCallbackData, TicTacToeResetCallbackData
from enums import Row, Who


def tic_tac_toe_inline_keyboard_builder(
    key: str, is_ended: bool, map: List[List[Who]]
) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for row_index, row in enumerate(map):
        for column_index, column in enumerate(row):
            builder.button(
                text=column.text(),
                callback_data=TicTacToeMoveCallbackData(
                    key=key,
                    row=row_index,
                    column=column_index,
                ),
            )

    if is_ended:
        builder.button(text="Reset", callback_data=TicTacToeResetCallbackData(key=key))

    builder.adjust(len(Row), repeat=True)
    return builder
