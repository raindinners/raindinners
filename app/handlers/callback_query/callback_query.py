from __future__ import annotations

from aiogram import Router

from .create import router as create_router
from .dig import setup_dig
from .tic_tac_toe import setup_tic_tac_toe


def setup() -> Router:
    router = Router()
    dig_router = setup_dig()
    tic_tac_toe_router = setup_tic_tac_toe()

    router.include_routers(create_router, dig_router, tic_tac_toe_router)

    return router
