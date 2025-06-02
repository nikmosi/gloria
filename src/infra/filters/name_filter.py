from collections.abc import Iterable

from domain import MessageFilter
from domain.models.message import RawMessage


class NameMessageFilter(MessageFilter):
    def __init__(self, name: Iterable[str]) -> None:
        self.name = name

    def is_match(self, msg: RawMessage) -> bool:
        return msg.author in self.name
