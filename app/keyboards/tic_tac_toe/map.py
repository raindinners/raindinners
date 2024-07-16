from __future__ import annotations

from typing import List

from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback_data import TicTacToeMoveCallbackData, TicTacToeResetCallbackData
from enums import TicTacToeRow, TicTacToeWho


def map_inline_keyboard_builder(
    key: str, is_ended: bool, map: List[List[TicTacToeWho]]
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

    builder.adjust(len(TicTacToeRow), repeat=True)
    return builder
