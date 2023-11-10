from __future__ import annotations

from typing import TYPE_CHECKING

from raindinners.methods.base import Method, Request
from raindinners.types import User

if TYPE_CHECKING:
    from raindinners.rain_dinners import RainDinners


class GetMe(Method[User]):
    """
    Use this method to get information about current user.

    Parameters
      Name            | Type   | Required | Description

      1. access_token | String | Yes      | Auth access token

    Result
      :class:`User`
    """

    __name__ = "users/getMe"
    __returning__ = User

    access_token: str

    def request(self, interface: RainDinners) -> Request:
        return Request(method=self.__name__, data=self.model_dump())
