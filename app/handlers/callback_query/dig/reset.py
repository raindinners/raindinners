from __future__ import annotations

from aiogram import Bot, Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from callback_data import DigMoveCallbackData
from filters import As
from keyboards import d_map_inline_keyboard_builder
from schemas import Dig

from ._text import get_turn_text

router = Router()


@router.callback_query(
    DigMoveCallbackData.filter(),
    As("dig", Dig),
)
async def dig_reset_handler(
    callback_query: CallbackQuery,
    callback_data: DigMoveCallbackData,
    bot: Bot,
    dig: Dig,
) -> Dig:
    dig.reset()

    await bot.edit_message_text(
        text=get_turn_text(current=dig.current),
        inline_message_id=callback_data.key,
        parse_mode=ParseMode.MARKDOWN,
    )
    await bot.edit_message_reply_markup(
        inline_message_id=callback_data.key,
        reply_markup=d_map_inline_keyboard_builder(
            key=callback_data.key, is_ended=True, map=dig.map
        ).as_markup(),
    )
    await callback_query.answer(text="Another one?")

    return dig
