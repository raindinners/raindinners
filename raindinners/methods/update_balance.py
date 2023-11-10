from __future__ import annotations

from typing import TYPE_CHECKING

from raindinners.methods.base import Method, Request

if TYPE_CHECKING:
    from raindinners.raindinners import RainDinners


class UpdateBalance(Method[bool]):
    """
    Use this method to update user balance.

    Parameters
      Name         | Type    | Required | Description

      1. user_id   | Integer | Yes      | Auth access token
      2. balance   | Integer | Yes      | New balance (send +200 or -200)
      3. bot_token | String  | Yes      | Bot token to restrict method usage

    Result
      :class:`bool`
    """

    __name__ = "users/updateBalance"
    __returning__ = bool

    user_id: int
    balance: int
    bot_token: str

    def request(self, rain_dinners: RainDinners) -> Request:
        return Request(method=self.__name__, data=self.model_dump())
