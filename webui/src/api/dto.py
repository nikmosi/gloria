from __future__ import annotations

from datetime import datetime
from typing import List

from pydantic import BaseModel, Field, field_validator


class MessagesQuery(BaseModel):
    """Query parameters for messages listing."""

    page: int = 1
    page_size: int = 50
    sort: List[str] = Field(default_factory=lambda: ["position", "date"])
    order: List[str] = Field(default_factory=lambda: ["asc", "desc"])
    author: str | None = None
    date_from: datetime | None = None
    date_to: datetime | None = None
    q: str | None = None

    @field_validator("sort", "order", mode="before")
    @classmethod
    def split_csv(cls, v: str | list[str]) -> list[str]:
        if isinstance(v, str):
            return [item for item in v.split(",") if item]
        return v
