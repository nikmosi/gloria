from collections.abc import Iterable

from loguru import logger

from domain.values import RawMessage
from logic.messages.filter import MessageFilter


class NameMessageFilter(MessageFilter):
    def __init__(self, names: Iterable[str]) -> None:
        self.names = set(names)
        logger.debug(f"{self.names=}")

    def is_match(self, msg: RawMessage) -> bool:
        passed = msg.author in self.names
        if passed:
            logger.info(f"[blue bold]passed[/]: {msg.text}...")
        else:
            logger.debug(f"[red bold]filtered[/]: {msg.text[:10]}...")
        return passed
