from __future__ import annotations

import asyncio
from collections import defaultdict
from enum import Enum
from typing import TYPE_CHECKING, Any, AsyncGenerator, Dict, List, Optional, cast

from aiohttp import FormData
from aiohttp.client import ClientError, ClientSession

from raindinners.exceptions import RainDinnersNetworkError
from raindinners.methods import Method, RainDinnersType
from raindinners.utils.response_validator import response_validator

if TYPE_CHECKING:
    from raindinners.rain_dinners import RainDinners


class DataManager:
    def prepare_value(self, value: Any, files: Optional[Dict[str, Any]] = None) -> Any:
        if value is None:
            return None
        if isinstance(value, str):
            return value
        if isinstance(value, Dict):
            value = {
                key: prepared_item
                for key, item in value.items()
                if (prepared_item := self.prepare_value(item, files=files)) is not None
            }

            return value
        if isinstance(value, List):
            value = [
                prepared_item
                for item in value
                if (prepared_item := self.prepare_value(item, files=files)) is not None
            ]

            return value
        if isinstance(value, Enum):
            return self.prepare_value(value.value, files=files)

        return value

    def build_form_data(self, method: Method) -> FormData:
        form = FormData(quote_fields=False)

        for key, value in method.model_dump().items():
            if value := self.prepare_value(value):
                form.add_field(key, value)

        return form


class SessionManager:
    def __init__(
        self,
        session: Optional[ClientSession] = None,
        *,
        connect_kwargs: Dict[str, Any] = defaultdict(),  # noqa
    ) -> None:
        self.session = session
        self.connect_kwargs = connect_kwargs
        self.should_reset_connector = not self.session

    async def create(self) -> None:
        if self.should_reset_connector:
            await self.close()
        if self.session is None or self.session.closed:
            self.session = ClientSession(**self.connect_kwargs)
            self.should_reset_connector = False

    async def close(self) -> None:
        if self.session and not self.session.closed:
            await self.session.close()


class Session(SessionManager, DataManager):
    def __init__(
        self,
        *,
        session: Optional[ClientSession] = None,
        connect_kwargs: Dict[str, Any] = defaultdict(),  # noqa
    ) -> None:
        super(Session, self).__init__(
            session=session,
            connect_kwargs=connect_kwargs,
        )

    async def request(
        self, rain_dinners: RainDinners, method: Method[RainDinnersType], timeout: int = 60
    ) -> RainDinnersType:
        await self.create()

        try:
            async with self.session.post(
                url=rain_dinners.network.url(method=method.__name__),
                json={
                    key: self.prepare_value(value)
                    for key, value in method.request(rain_dinners=rain_dinners).data.items()
                },
                timeout=timeout,
            ) as response:
                content = await response.text()
        except asyncio.TimeoutError:
            raise RainDinnersNetworkError("Exception %s: %s." % (method, "request timeout error"))
        except ClientError as e:
            raise RainDinnersNetworkError(
                "Exception for method %s: %s." % (method.__name__, f"{type(e).__name__}: {e}")
            )

        response = response_validator(method=method, status_code=response.status, content=content)
        return cast(RainDinnersType, response.result)

    async def stream(
        self,
        rain_dinners: RainDinners,
        file_id: str,
        timeout: int = 60,
        chunk_size: int = 65536,
        raise_for_status: bool = True,
    ) -> AsyncGenerator[bytes, None]:
        await self.create()

        async with self.session.post(
            url=rain_dinners.network.file(file_id=file_id),
            timeout=timeout,
            raise_for_status=raise_for_status,
        ) as response:
            async for chunk in response.content.iter_chunked(chunk_size):
                yield chunk
