from __future__ import annotations

from aiogram.filters.callback_data import CallbackData


class CreateCallbackData(CallbackData, prefix="create"):
    game: str
