from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, Optional, Self

from sqlalchemy.orm import Mapped, Session, mapped_column, relationship

from metadata import BALANCE_DEFAULT, BONUS_AMOUNT, BONUS_INCREMENT_TIME_HOURS

from .core import ORMModel, types

if TYPE_CHECKING:
    from .user import UserModel


class BalanceModel(ORMModel):
    balance: Mapped[types.BigInt] = mapped_column(default=BALANCE_DEFAULT)
    bonus_increment_time_hours: Mapped[types.BigInt] = mapped_column(
        default=BONUS_INCREMENT_TIME_HOURS
    )
    last_time_claimed_bonus: Mapped[Optional[datetime.datetime]] = mapped_column(nullable=True)

    user_id: Mapped[types.UserID]
    user: Mapped[Optional[UserModel]] = relationship(back_populates="balance")

    @classmethod
    def _joinedload_support(cls) -> bool:
        return False

    @classmethod
    def take_bonus(
        cls,
        session: Session,
        /,
        id: int,
        bonus_increment_time_hours: int,
        bonus_amount: int = BONUS_AMOUNT,
    ) -> Self:
        return cls.s_update(
            session,
            values={
                BalanceModel.balance: BalanceModel.balance + bonus_amount,
                BalanceModel.last_time_claimed_bonus: datetime.datetime.now()
                + datetime.timedelta(hours=bonus_increment_time_hours),
            },
            id=id,
        )
