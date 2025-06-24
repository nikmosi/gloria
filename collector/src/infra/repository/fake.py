from typing import override

from loguru import logger

from domain.repository import MessageRepository
from domain.values import ParsedMessage


class FakeRepository(MessageRepository):
    def __init__(self) -> None:
        self._messages: list[ParsedMessage] = []
        super().__init__()

    def get_saved(self) -> list[ParsedMessage]:
        return list(self._messages)

    @override
    async def save(self, msg: ParsedMessage) -> None:
        self._messages.append(msg)
        logger.debug(msg.model_dump_json())
