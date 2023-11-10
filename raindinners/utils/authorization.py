from __future__ import annotations

import datetime
import hashlib
import hmac
from typing import Optional

from raindinners.methods import SignIn


def create_telegram_authorization(
    bot_token: str,
    telegram_id: int,
    first_name: str,
    last_name: Optional[str],
    username: Optional[str],
    auth_date: datetime.datetime,
) -> SignIn:
    auth_date = int(auth_date.astimezone(tz=datetime.timezone.utc).timestamp())

    string = "\n".join(
        [
            f"{key}={value}"
            for key, value in sorted(
                {
                    "id": telegram_id,
                    "first_name": first_name,
                    "last_name": last_name,
                    "username": username,
                    "auth_date": auth_date,
                }.items(),
                key=lambda x: x[0],
            )
        ]
    )
    secret_key = hashlib.sha256(bot_token.encode()).digest()

    return SignIn(
        telegram_id=telegram_id,
        first_name=first_name,
        last_name=last_name,
        username=username,
        auth_date=auth_date,
        hash=hmac.new(secret_key, msg=string.encode(), digestmod=hashlib.sha256).hexdigest(),
    )
