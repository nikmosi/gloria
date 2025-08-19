from datetime import datetime

from pony.orm import PrimaryKey, Required

from . import db


class Message(db.Entity):
    """History of collected messages."""

    _table_ = "messages"

    id = PrimaryKey(int, auto=True)
    nickname = Required(str)
    date = Required(datetime)
    points = Required(int)
    hours = Required(float)
    position = Required(int)
    rank_name = Required(str)
    rank_left = Required(int)
    rank_right = Required(int)


class LastMessage(db.Entity):
    """Latest message per nickname."""

    _table_ = "last_messages"

    nickname = PrimaryKey(str)
    date = Required(datetime)
    points = Required(int)
    hours = Required(float)
    position = Required(int)
    rank_name = Required(str)
    rank_left = Required(int)
    rank_right = Required(int)


__all__ = ["Message", "LastMessage"]
