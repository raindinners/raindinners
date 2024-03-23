from __future__ import annotations

from aiogram import Router

from .create import router as create_router
from .tic_tac_toe import setup_tic_tac_toe


def setup() -> Router:
    router = Router()
    tic_tac_toe_router = setup_tic_tac_toe()

    router.include_routers(create_router, tic_tac_toe_router)

    return router
