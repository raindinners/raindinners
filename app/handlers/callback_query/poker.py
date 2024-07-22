from __future__ import annotations

from aiogram import Router
from aiogram.types import CallbackQuery
from redis.asyncio import Redis

from _redis import save
from callback_data import PokerCallbackData
from utils.poker import get_poker

router = Router()


@router.callback_query(PokerCallbackData.filter())
async def poker_handler(
    callback_query: CallbackQuery,
    redis: Redis,
    callback_data: PokerCallbackData,
) -> None:
    poker = await get_poker(redis=redis, poker=callback_data.inline_message_id)
    if callback_data.type == "join":
        poker.engine.players.add_player(
            stack=poker.engine.traits.bb_bet * poker.engine.traits.bb_mult,
            id=f"{callback_query.from_user.id}_{callback_query.from_user.first_name}",
        )
    else:
        poker.engine.players.remove_player(
            id=f"{callback_query.from_user.id}_{callback_query.from_user.first_name}",
        )

    await save(redis=redis, key=callback_data.inline_message_id, value=poker)

    await callback_query.answer(text=callback_data.type.capitalize())
