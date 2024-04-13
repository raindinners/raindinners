from __future__ import annotations

from typing import Optional

from aiogram import Bot, Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from callback_data import TicTacToeMoveCallbackData
from enums import TicTacToeColumn, TicTacToeRow
from filters import As
from keyboards import ttt_map_inline_keyboard_builder
from schemas import Player, TicTacToe

from ._text import get_move_end_text

router = Router()


@router.callback_query(
    TicTacToeMoveCallbackData.filter(),
    As("tic_tac_toe", TicTacToe),
)
async def tic_tac_toe_move_handler(
    callback_query: CallbackQuery,
    callback_data: TicTacToeMoveCallbackData,
    bot: Bot,
    tic_tac_toe: TicTacToe,
) -> Optional[TicTacToe]:
    if tic_tac_toe.is_ended:
        if not tic_tac_toe.winner:
            return await callback_query.answer(text="What are you gonna win here?")
        if tic_tac_toe.winner.user_id == callback_query.from_user.id:
            return await callback_query.answer(text="Dumb? You already win...")

        return await callback_query.answer(text="Looser!")

    player = Player(
        user_id=callback_query.from_user.id, full_name=callback_query.from_user.full_name
    )

    tic_tac_toe.add_player(player=player)
    if not tic_tac_toe.in_game(player):
        return await callback_query.answer(text="Nice try bro, but I got you!")

    if tic_tac_toe.player_turn(player):
        if not tic_tac_toe.move(
            row=TicTacToeRow(callback_data.row), column=TicTacToeColumn(callback_data.column)
        ):
            return await callback_query.answer(
                text="Bro, is that question marks doesn't carry you???"
            )
    else:
        return await callback_query.answer(text="Comeback on your turn...")

    await bot.edit_message_text(
        text=get_move_end_text(
            is_ended=tic_tac_toe.is_ended, winner=tic_tac_toe.winner, current=tic_tac_toe.current
        ),
        inline_message_id=callback_data.key,
        parse_mode=ParseMode.MARKDOWN,
    )
    await bot.edit_message_reply_markup(
        inline_message_id=callback_data.key,
        reply_markup=ttt_map_inline_keyboard_builder(
            key=callback_data.key, is_ended=tic_tac_toe.is_ended, map=tic_tac_toe.map
        ).as_markup(),
    )

    return tic_tac_toe
