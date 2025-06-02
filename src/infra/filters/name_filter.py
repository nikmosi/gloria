from collections.abc import Iterable

from loguru import logger

from domain import MessageFilter
from domain.models.message import RawMessage


class NameMessageFilter(MessageFilter):
    def __init__(self, name: Iterable[str]) -> None:
        self.name = name

    def is_match(self, msg: RawMessage) -> bool:
        passed = msg.author in self.name
        if not passed:
            logger.info(f"[blue bold]filtered[/]: {msg.text[:10]}...")
        return passed
