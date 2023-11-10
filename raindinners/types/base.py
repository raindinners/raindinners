from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Extra


class RainDinnersObject(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra=Extra.allow,
        validate_assignment=True,
        populate_by_name=True,
        use_enum_values=True,
    )


class MutableRainDinnersObject(RainDinnersObject):
    model_config = ConfigDict(
        frozen=False,
    )
