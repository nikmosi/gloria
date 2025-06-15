from typing import override

from loguru import logger

from domain.repository import MessageRepository
from domain.values import ParsedMessage


class FakeRepository(MessageRepository):
    def __init__(self) -> None:
        super().__init__()

    @override
    async def save(self, msg: ParsedMessage) -> None:
        logger.debug(msg.model_dump_json())
