from __future__ import annotations

import time
from typing import Any, List

from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent

from enums import Games
from keyboards import create_inline_keyboard_builder

router = Router()


def get_create_results() -> List[Any]:
    return [
        InlineQueryResultArticle(
            id=str(time.time()),
            title=Games.TIC_TAC_TOE,
            input_message_content=InputTextMessageContent(
                message_text="Just click button below", parse_mode=ParseMode.MARKDOWN
            ),
            reply_markup=create_inline_keyboard_builder(game=Games.TIC_TAC_TOE).as_markup(),
        )
    ]


@router.inline_query()
async def create_handler(inline_query: InlineQuery) -> None:
    await inline_query.answer(results=get_create_results())  # mypy: ignore[arg-type]
