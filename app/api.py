from __future__ import annotations

import datetime
import random
from typing import Any, Dict, List, Tuple

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from distributed_websocket import WebSocketManager
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Body, Depends, Path
from fastapi.requests import Request
from fastapi.websockets import WebSocket
from pokerengine.card import Cards
from pokerengine.engine import EngineTraits
from pokerengine.evaluation import get_evaluation_result
from redis.asyncio import Redis
from sqlalchemy.orm import Session

from _redis import save
from api_protect import is_allowed
from core.depends import (
    get_redis,
    get_redis_from_request,
    get_scheduler_from_request,
    get_sync_session,
    get_websocket_manager,
    get_websocket_manager_from_request,
)
from core.poker import game
from core.settings import server_settings
from metadata import RANDOM_MAX_VALUE, RANDOM_MIN_VALUE
from orm import BalanceModel, UserModel
from poker import Poker
from requests import (
    CreateRequest,
    GetEvaluationResultRequest,
    GetUserRequest,
    RememberUserRequest,
    TakeBonusRequest,
)
from schemas import ApplicationResponse
from schemas.orm import User
from utils.id import generate_id
from ws import websocket_handler

router = APIRouter()


@router.websocket(path="/{user_id}")
async def web_poker_main_websocket_handler(
    websocket: WebSocket,
    manager: WebSocketManager = Depends(get_websocket_manager),
    redis: Redis = Depends(get_redis),
    user_id: str = Path(...),
) -> None:
    if not server_settings.DEBUG and is_allowed(websocket.client.host):
        raise HTTPException(
            detail="NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    connection = await manager.new_connection(websocket=websocket, conn_id=user_id)
    try:
        await websocket_handler(connection=connection, manager=manager, redis=redis)
    except Exception:  # noqa
        manager.remove_connection(connection)


@router.post(
    path="/rememberUser",
    response_model=ApplicationResponse[bool],
    status_code=status.HTTP_200_OK,
)
def remember_user_handler(
    request: Request,
    request_body: RememberUserRequest = Body(...),
    session: Session = Depends(get_sync_session),
) -> Dict[str, Any]:
    if not server_settings.DEBUG and is_allowed(request.client.host):
        raise HTTPException(
            detail="NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    if UserModel.s_get_by_id(session, id=request_body.user_id):
        return {
            "ok": True,
            "result": True,
        }

    user = UserModel.s_create(session, values={UserModel.id: request_body.user_id})
    BalanceModel.s_create(session, values={BalanceModel.user_id: user.id})

    return {
        "ok": True,
        "result": True,
    }


@router.post(
    path="/getUser",
    response_model=ApplicationResponse[User],
    status_code=status.HTTP_200_OK,
)
def get_user_handler(
    request_body: GetUserRequest = Body(...),
    session: Session = Depends(get_sync_session),
) -> Dict[str, Any]:
    user = UserModel.s_get_by_id(session, id=request_body.user_id)
    if not user:
        raise HTTPException(
            detail="NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return {
        "ok": True,
        "result": user,
    }


@router.post(
    path="/takeBonus",
    response_model=ApplicationResponse[bool],
    status_code=status.HTTP_200_OK,
)
def take_bonus_handler(
    request: Request,
    request_body: TakeBonusRequest = Body(...),
    session: Session = Depends(get_sync_session),
) -> Dict[str, Any]:
    if not server_settings.DEBUG and is_allowed(request.client.host):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    user = UserModel.s_get_by_id(session, id=request_body.user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if (
        user.balance.last_time_claimed_bonus
        and user.balance.last_time_claimed_bonus
        + datetime.timedelta(hours=user.balance.bonus_increment_time_hours)
        > datetime.datetime.now()
    ):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    BalanceModel.take_bonus(
        session,
        id=user.balance.id,
        bonus_increment_time_hours=user.balance.bonus_increment_time_hours,
    )

    return {
        "ok": True,
        "result": True,
    }


@router.post(
    path="/createPoker",
    response_model=ApplicationResponse[str],
    status_code=status.HTTP_200_OK,
)
async def create_poker_handler(
    request: Request,
    request_body: CreateRequest = Body(...),
    manager: WebSocketManager = Depends(get_websocket_manager_from_request),
    redis: Redis = Depends(get_redis_from_request),
    scheduler: AsyncIOScheduler = Depends(get_scheduler_from_request),
) -> Dict[str, Any]:
    if not server_settings.DEBUG and is_allowed(request.client.host):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    poker = generate_id()
    await save(
        redis=redis,
        key=poker,
        value=Poker(
            traits=EngineTraits(
                sb_bet=request_body.sb_bet,
                bb_bet=request_body.bb_bet,
                bb_mult=request_body.bb_mult,
                min_raise=request_body.min_raise or request_body.bb_bet,
            ),
            seed=random.randint(RANDOM_MIN_VALUE, RANDOM_MAX_VALUE),
        ),
    )
    scheduler.add_job(
        game,
        kwargs={
            "manager": manager,
            "redis": redis,
            "poker": poker,
        },
        trigger="interval",
        id=poker,
        max_instances=1,
        seconds=1,
    )

    return {
        "ok": True,
        "result": poker,
    }


@router.post(
    path="/pokerGetEvaluationResult",
    response_model=ApplicationResponse[List[Tuple[str, int]]],
    status_code=status.HTTP_200_OK,
)
def get_evaluation_result_handler(
    request_body: GetEvaluationResultRequest = Body(...),
) -> Dict[str, Any]:
    return {
        "ok": True,
        "result": [
            (str(result), index)
            for result, index in get_evaluation_result(
                cards=Cards(board=request_body.board, hands=request_body.hands),
                players=request_body.players,
            )
        ],
    }
