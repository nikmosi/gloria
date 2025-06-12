from collections.abc import Iterable

from loguru import logger

from domain import MessageFilter
from domain.values import RawMessage


class NameMessageFilter(MessageFilter):
    def __init__(self, names: Iterable[str]) -> None:
        self.names = set(names)

    def is_match(self, msg: RawMessage) -> bool:
        passed = msg.author in self.names
        if not passed:
            logger.info(f"[blue bold]filtered[/]: {msg.text[:10]}...")
        return passed
