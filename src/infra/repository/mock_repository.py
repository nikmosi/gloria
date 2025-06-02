from typing import override

from loguru import logger

from domain.models import ParsedMessage
from domain.repository import MessageRepository


class MockRepository(MessageRepository):
    def __init__(self) -> None:
        super().__init__()

    @override
    def save(self, msg: ParsedMessage) -> None:
        logger.debug(msg.model_dump_json())
