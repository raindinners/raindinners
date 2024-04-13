from __future__ import annotations

from aiogram.filters.callback_data import CallbackData


class MoveCallbackData(CallbackData, prefix="d_move"):
    key: str
    row: int
    index: int
