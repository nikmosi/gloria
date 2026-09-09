from collections.abc import Iterable

from loguru import logger

from domain.values import RawMessage
from logic.messages.filter import MessageFilter


class NameMessageFilter(MessageFilter):
    def __init__(self, names: Iterable[str]) -> None:
        self.names = set(names)
        logger.debug(f"Initialized NameMessageFilter with names: {self.names}")

    def is_match(self, msg: RawMessage) -> bool:
        return msg.author in self.names
