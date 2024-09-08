from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class BaseParams(BaseModel):
    def to_query_string(self) -> str:
        dict_model = self.model_dump()
        for key, value in dict_model.items():
            if isinstance(value, list):
                dict_model[key] = "" if not value else ",".join(str(v) for v in value)

        return "&".join(f"{k}={v}" for k, v in dict_model.items() if v is not None)


class GachaParams(BaseParams, frozen=False):
    account_id: str
    uid: int = 0
    banner_type: str
    """
    原神：角色祈愿、武器祈愿、常驻祈愿、新手祈愿、集录祈愿
    """
    rarities: list[int] = Field(default_factory=list)
    size: int = 100
    page: int = 1
    name_contains: str | None = None

    @field_validator("rarities", mode="before")
    @classmethod
    def __parse_rarities(cls, value: str | list[int]) -> list[int]:
        if isinstance(value, list):
            return value
        if not value:
            return []
        return [int(rarity) for rarity in value.split(",")]
