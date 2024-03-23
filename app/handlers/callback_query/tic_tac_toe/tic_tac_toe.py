from __future__ import annotations

from aiogram import Router

from .move import router as move_router
from .reset import router as reset_router


def setup() -> Router:
    router = Router()
    router.include_routers(move_router, reset_router)

    return router
