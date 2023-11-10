from __future__ import annotations

import abc
from typing import TYPE_CHECKING, Any, Dict, Generic, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Extra

if TYPE_CHECKING:
    from raindinners.raindinners import RainDinners

RainDinnersType = TypeVar("RainDinnersType")


class Request(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    method: str
    data: Dict[str, Any]
    files: Optional[Dict[str, Any]] = None


class Response(BaseModel, Generic[RainDinnersType]):
    ok: bool
    result: Optional[RainDinnersType] = None
    error: Optional[str] = None
    error_code: Optional[int] = None


class Method(abc.ABC, BaseModel, Generic[RainDinnersType]):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra=Extra.allow,
        populate_by_name=True,
    )

    @property
    @abc.abstractmethod
    def __name__(self) -> str:
        ...

    @property
    @abc.abstractmethod
    def __returning__(self) -> Any:
        ...

    @abc.abstractmethod
    def request(self, rain_dinners: RainDinners) -> Request:
        ...

    def response(self, data: Dict[str, Any]) -> Response[RainDinnersType]:
        return Response[self.__returning__].model_validate(data)  # type: ignore[name-defined]
