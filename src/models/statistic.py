from datetime import datetime

from pydantic import BaseModel


class Rank(BaseModel):
    name: str
    left: int
    right: int


class StatisticMessage(BaseModel):
    date: datetime
    nickname: str
    points: int
    hours: float
    position: int
    rank: Rank
