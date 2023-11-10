from __future__ import annotations

from typing import TYPE_CHECKING

from raindinners.methods.base import Method, Request

if TYPE_CHECKING:
    from raindinners.raindinners import RainDinners


class GetBonus(Method[bool]):
    """
    Use this method to get balance bonus.

    Parameters
      Name            | Type   | Required | Description

      1. access_token | String | Yes      | Auth access token

    Result
      :class:`bool`
    """

    __name__ = "users/getBonus"
    __returning__ = bool

    access_token: str

    def request(self, raindinners: RainDinners) -> Request:
        return Request(method=self.__name__, data=self.model_dump())
