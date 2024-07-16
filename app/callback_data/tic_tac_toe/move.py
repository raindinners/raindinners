from __future__ import annotations

from aiogram.filters.callback_data import CallbackData


class MoveCallbackData(CallbackData, prefix="ttt_move"):
    key: str
    row: int
    column: int
