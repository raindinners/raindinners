from __future__ import annotations

from aiogram.filters.callback_data import CallbackData


class ResetCallbackData(CallbackData, prefix="tic_tac_toe_reset"):
    key: str
