from __future__ import annotations

from typing import TYPE_CHECKING

from raindinners.methods.base import Method, Request
from raindinners.types import User

if TYPE_CHECKING:
    from raindinners.rain_dinners import RainDinners


class GetUser(Method[User]):
    """
    Use this method to get information about any user.

    Parameters
      Name       | Type    | Required | Description

      1. user_id | Integer | Yes      | User ID in the system

    Result
      :class:`User`
    """

    __name__ = "users/getUser"
    __returning__ = User

    user_id: int

    def request(self, interface: RainDinners) -> Request:
        return Request(method=self.__name__, data=self.model_dump())
