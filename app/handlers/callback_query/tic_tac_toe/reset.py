from __future__ import annotations

from aiogram import Bot, Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from callback_data import TicTacToeResetCallbackData
from filters import As
from keyboards import ttt_map_inline_keyboard_builder
from schemas import TicTacToe

from ._text import get_turn_text

router = Router()


@router.callback_query(
    TicTacToeResetCallbackData.filter(),
    As("tic_tac_toe", TicTacToe),
)
async def tic_tac_toe_reset_handler(
    callback_query: CallbackQuery,
    callback_data: TicTacToeResetCallbackData,
    bot: Bot,
    tic_tac_toe: TicTacToe,
) -> TicTacToe:
    tic_tac_toe.reset()

    await bot.edit_message_text(
        text=get_turn_text(current=tic_tac_toe.current),
        inline_message_id=callback_data.key,
        parse_mode=ParseMode.MARKDOWN,
    )
    await bot.edit_message_reply_markup(
        inline_message_id=callback_data.key,
        reply_markup=ttt_map_inline_keyboard_builder(
            key=callback_data.key, is_ended=True, map=tic_tac_toe.map
        ).as_markup(),
    )
    await callback_query.answer(text="Another one?")

    return tic_tac_toe
