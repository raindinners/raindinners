from __future__ import annotations

from typing import Optional

from aiogram import Bot, Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from callback_data import DigMoveCallbackData
from filters import As
from keyboards import d_map_inline_keyboard_builder
from schemas import Dig, Player

from ._text import get_move_end_text

router = Router()


@router.callback_query(
    DigMoveCallbackData.filter(),
    As("dig", Dig),
)
async def dig_move_handler(
    callback_query: CallbackQuery,
    callback_data: DigMoveCallbackData,
    bot: Bot,
    dig: Dig,
) -> Optional[Dig]:
    if dig.winner:
        return await callback_query.answer(text="The diamonds are out (:")

    player = Player(
        user_id=callback_query.from_user.id, full_name=callback_query.from_user.full_name
    )

    dig.add_player(player=player)
    if not dig.in_game(player):
        return await callback_query.answer(text="You don't have a shovel to dig...")

    if dig.player_turn(player):
        if not dig.move(row=callback_data.row, index=callback_data.index):
            return await callback_query.answer(text="You're looking in the wrong place.")
    else:
        return await callback_query.answer(text="You still have time to dig")

    await bot.edit_message_text(
        text=get_move_end_text(winner=dig.winner, current=dig.current),
        inline_message_id=callback_data.key,
        parse_mode=ParseMode.MARKDOWN,
    )
    await bot.edit_message_reply_markup(
        inline_message_id=callback_data.key,
        reply_markup=d_map_inline_keyboard_builder(
            key=callback_data.key, is_ended=bool(dig.winner), map=dig.map
        ).as_markup(),
    )

    return dig
