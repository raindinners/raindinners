from __future__ import annotations

from aiogram import Bot, F, Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from callback_data import CreateCallbackData
from enums import Games
from filters import As
from keyboards import d_map_inline_keyboard_builder, ttt_map_inline_keyboard_builder
from schemas import Dig, TicTacToe

router = Router()


@router.callback_query(
    CreateCallbackData.filter(F.game == Games.TIC_TAC_TOE.name),
    As("tic_tac_toe", TicTacToe, default=TicTacToe()),
)
async def create_tic_tac_toe_handler(
    callback_query: CallbackQuery, bot: Bot, tic_tac_toe: TicTacToe
) -> TicTacToe:
    tic_tac_toe.key = callback_query.inline_message_id
    tic_tac_toe.reset()

    await bot.edit_message_text(
        text="Tap any field",
        inline_message_id=callback_query.inline_message_id,
        parse_mode=ParseMode.MARKDOWN,
    )
    await bot.edit_message_reply_markup(
        inline_message_id=callback_query.inline_message_id,
        reply_markup=ttt_map_inline_keyboard_builder(
            key=tic_tac_toe.key, is_ended=False, map=tic_tac_toe.map
        ).as_markup(),
    )

    return tic_tac_toe


@router.callback_query(
    CreateCallbackData.filter(F.game == Games.DIG.name),
    As("dig", Dig, default=Dig()),
)
async def create_dig_handler(callback_query: CallbackQuery, bot: Bot, dig: Dig) -> Dig:
    dig.key = callback_query.inline_message_id
    dig.reset()

    await bot.edit_message_text(
        text="Tap any field",
        inline_message_id=callback_query.inline_message_id,
        parse_mode=ParseMode.MARKDOWN,
    )
    await bot.edit_message_reply_markup(
        inline_message_id=callback_query.inline_message_id,
        reply_markup=d_map_inline_keyboard_builder(
            key=dig.key, is_ended=False, map=dig.map
        ).as_markup(),
    )

    return dig
