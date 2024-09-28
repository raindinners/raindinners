from __future__ import annotations

from typing import Any, Dict, Optional, Self, cast

import stringcase
from sqlalchemy import Result, ScalarResult, insert, select, update
from sqlalchemy.orm import (
    DeclarativeBase,
    Session,
    declared_attr,
    joinedload,
    mapped_column,
)
from sqlalchemy.orm.attributes import Mapped

from .types import BigInt


class ORMModel(DeclarativeBase):
    id: Mapped[BigInt] = mapped_column(unique=True, primary_key=True)

    @declared_attr  # type: ignore
    def __tablename__(cls) -> str:  # noqa
        return cast(str, stringcase.snakecase(cls.__name__.split("Model")[0]) + "s")

    @classmethod
    def _rows(cls, result: Result[Any]) -> ScalarResult[Any]:
        return result.scalars()

    @classmethod
    def _one_row(cls, scalar_result: ScalarResult[Any]) -> Optional[Self]:
        return scalar_result.one_or_none()

    @classmethod
    def _where_for_all_attributes(
        cls,
        statement: Any,
        /,
        **kwargs: Any,
    ) -> Any:
        return statement.where(
            *[
                getattr(cls, __attr__) == kwargs.get(__attr__)
                for __attr__ in cls.__dict__
                if not __attr__.startswith("__")
                and not __attr__.endswith("__")
                and not __attr__.startswith("_")
                and kwargs.get(__attr__, None)
            ]
        )

    @classmethod
    def _joinedload_support(cls) -> bool:
        return bool(
            [
                __attr__
                for __attr__ in cls.__dict__
                if not __attr__.startswith("__")
                or not __attr__.endswith("__")
                or not __attr__.startswith("_")
                and ORMModel in getattr(cls, __attr__).class_.__mro__
            ]
        )

    @classmethod
    def _joinedload_for_all(cls, statement: Any) -> Any:
        return statement.options(
            *[
                joinedload(getattr(cls, __attr__))
                for __attr__ in cls.__dict__
                if not __attr__.startswith("__")
                and not __attr__.endswith("__")
                and not __attr__.startswith("_")
                and ORMModel in getattr(cls, __attr__).class_.__mro__
            ]
        )

    @classmethod
    def s_create(cls, session: Session, /, values: Dict[str, Any]) -> Self:
        statement = insert(cls)
        return cls._one_row(
            scalar_result=cls._rows(
                result=session.execute(statement.values(values).returning(cls))
            )
        )

    @classmethod
    def s_update(cls, session: Session, /, values: Dict[str, Any], **kwargs: Any) -> Self:
        statement = update(cls)
        return cls._one_row(
            scalar_result=cls._rows(
                result=session.execute(
                    cls._where_for_all_attributes(statement, **kwargs)
                    .values(values)
                    .returning(cls)
                )
            )
        )

    @classmethod
    def s_get_by_id(cls, session: Session, /, id: int) -> Self:
        statement = select(cls)
        if cls._joinedload_support():
            cls._joinedload_for_all(statement=statement)

        return cls._one_row(
            scalar_result=cls._rows(result=session.execute(statement.where(cls.id == id)))
        )

    @classmethod
    def s_get_one_by(cls, session: Session, /, **kwargs: Any) -> Optional[Self]:
        statement = select(cls)
        if cls._joinedload_support():
            cls._joinedload_for_all(statement=statement)

        return cls._one_row(
            scalar_result=cls._rows(
                result=session.execute(cls._where_for_all_attributes(statement, **kwargs))
            )
        )
