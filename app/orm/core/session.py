from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.settings import database_settings, server_settings
from metadata import POOL_RECYCLE

async_engine = create_async_engine(
    database_settings.async_url,
    pool_recycle=POOL_RECYCLE,
    isolation_level="SERIALIZABLE",
    echo=server_settings.DEBUG,
)
async_sessionmaker = sessionmaker(  # type: ignore[call-overload]
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

sync_engine = create_engine(
    database_settings.sync_url,
    pool_recycle=POOL_RECYCLE,
    isolation_level="SERIALIZABLE",
    # echo=server_settings.DEBUG,
)
sync_sessionmaker = sessionmaker(  # type: ignore[call-overload]
    bind=sync_engine,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)
