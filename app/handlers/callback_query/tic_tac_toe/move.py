from __future__ import annotations

from typing import Optional

from aiogram import Bot, Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from callback_data import TicTacToeMoveCallbackData
from enums import Column, Row, Who
from filters import As
from keyboards import tic_tac_toe_inline_keyboard_builder
from schemas import TicTacToe, TicTacToePlayer
from schemas.tic_tac_toe import Player

from ._text import get_move_end_text

router = Router()


def add_player(tic_tac_toe: TicTacToe, user_id: int, full_name: str) -> None:
    if not tic_tac_toe.x_player:
        tic_tac_toe.x_player = TicTacToePlayer(
            user_id=user_id,
            full_name=full_name,
        )

    if not tic_tac_toe.o_player and tic_tac_toe.x_player.user_id != user_id:
        tic_tac_toe.o_player = TicTacToePlayer(
            user_id=user_id,
            full_name=full_name,
        )


def is_in_game(user_id: int, x_player: Player, o_player: Player) -> bool:
    return x_player.user_id == user_id or o_player.user_id == user_id


def is_player_turn(user_id: int, current: Who, x_player: Player, o_player: Player) -> bool:
    return (current == Who.X and x_player.user_id == user_id) or (
        current == Who.O and o_player and o_player.user_id == user_id
    )


@router.callback_query(TicTacToeMoveCallbackData.filter(), As("tic_tac_toe", TicTacToe))
async def move_handler(
    callback_query: CallbackQuery,
    callback_data: TicTacToeMoveCallbackData,
    bot: Bot,
    tic_tac_toe: TicTacToe,
) -> Optional[TicTacToe]:
    if tic_tac_toe.is_ended:
        return await callback_query.answer(
            text="You don't swing fists after a fight!", show_alert=True
        )

    add_player(
        tic_tac_toe=tic_tac_toe,
        user_id=callback_query.from_user.id,
        full_name=callback_query.from_user.full_name,
    )
    if not is_in_game(
        user_id=callback_query.from_user.id,
        x_player=tic_tac_toe.x_player,
        o_player=tic_tac_toe.o_player,
    ):
        return await callback_query.answer(text="Nice try bro, but I got you!", show_alert=True)

    if is_player_turn(
        user_id=callback_query.from_user.id,
        current=tic_tac_toe.current,
        x_player=tic_tac_toe.x_player,
        o_player=tic_tac_toe.o_player,
    ):
        if not tic_tac_toe.move(row=Row(callback_data.row), column=Column(callback_data.column)):
            return await callback_query.answer(
                text="Bro, is that question marks doesn't carry you???", show_alert=True
            )
    else:
        return await callback_query.answer(text="Comeback on your turn...", show_alert=True)

    await bot.edit_message_text(
        text=get_move_end_text(
            is_ended=tic_tac_toe.is_ended,
            winner=tic_tac_toe.winner,
            current=tic_tac_toe.current,
            x_player=tic_tac_toe.x_player,
            o_player=tic_tac_toe.o_player,
        ),
        inline_message_id=callback_data.key,
        parse_mode=ParseMode.MARKDOWN,
    )
    await bot.edit_message_reply_markup(
        inline_message_id=callback_data.key,
        reply_markup=tic_tac_toe_inline_keyboard_builder(
            key=callback_data.key, is_ended=tic_tac_toe.is_ended, map=tic_tac_toe.map
        ).as_markup(),
    )

    return tic_tac_toe
