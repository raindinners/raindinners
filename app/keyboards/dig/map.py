from __future__ import annotations

from typing import List

from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback_data import DigMoveCallbackData, DigResetCallbackData
from enums import DigItem


def map_inline_keyboard_builder(
    key: str, is_ended: bool, map: List[List[DigItem]]
) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for row_index, row in enumerate(map):
        for column_index, column in enumerate(row):
            builder.button(
                text=column,
                callback_data=DigMoveCallbackData(key=key, row=row_index, index=column_index),
            )

    if is_ended:
        builder.button(text="Reset", callback_data=DigResetCallbackData(key=key))

    return builder
