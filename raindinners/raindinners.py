from __future__ import annotations

from collections import defaultdict
from typing import Any, AsyncGenerator, Dict, Optional

from aiohttp.client import ClientSession

from raindinners.methods import Method, RainDinnersType
from raindinners.network import Network
from raindinners.session import Session


class RainDinners:
    def __init__(
        self,
        network: Network,
        *,
        session: Optional[ClientSession] = None,
        connect_kwargs: Dict[str, Any] = defaultdict(),  # noqa
    ) -> None:
        self.network = network
        self.session = Session(session=session, connect_kwargs=connect_kwargs)

    async def request(self, method: Method[RainDinnersType], timeout: int = 60) -> RainDinnersType:
        return await self.session.request(raindinners=self, method=method, timeout=timeout)

    async def stream(
        self,
        file_id: str,
        timeout: int = 60,
        chunk_size: int = 65536,
    ) -> AsyncGenerator[bytes, None]:
        return self.session.stream(
            raindinners=self,
            file_id=file_id,
            timeout=timeout,
            chunk_size=chunk_size,
        )
