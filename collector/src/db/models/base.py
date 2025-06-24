from datetime import datetime
from typing import Any

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True

    def to_dict(self) -> dict[str, Any]:
        return {c.key: getattr(self, c.key) for c in self.__table__.columns}


class LastMessage(Base):
    __tablename__ = "last_messages"
    nickname: Mapped[str] = mapped_column(primary_key=True)
    date: Mapped[datetime]
    points: Mapped[int] = mapped_column(index=True)
    hours: Mapped[float]
    position: Mapped[int]
    rank_name: Mapped[str]
    rank_left: Mapped[int]
    rank_right: Mapped[int]


class HistoryMessage(Base):
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nickname: Mapped[str]
    date: Mapped[datetime]
    points: Mapped[int] = mapped_column(index=True)
    hours: Mapped[float]
    position: Mapped[int]
    rank_name: Mapped[str]
    rank_left: Mapped[int]
    rank_right: Mapped[int]
