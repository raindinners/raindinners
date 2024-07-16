from __future__ import annotations

from aiogram.filters.callback_data import CallbackData


class ResetCallbackData(CallbackData, prefix="ttt_reset"):
    key: str
