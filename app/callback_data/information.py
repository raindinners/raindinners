from __future__ import annotations

from aiogram.filters.callback_data import CallbackData


class InformationCallbackData(CallbackData, prefix="information"):
    inline_message_id: str
