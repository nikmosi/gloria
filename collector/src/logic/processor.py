from loguru import logger

from domain.repository import MessageRepository
from logic.messages.filter import MessageFilter
from logic.messages.parser import MessageParser
from logic.messages.source import MessageSource


class MessageProcessor:
    def __init__(
        self,
        source: MessageSource,
        filter_: MessageFilter,
        parser: MessageParser,
        repository: MessageRepository,
    ) -> None:
        self.source: MessageSource = source
        self.filter_: MessageFilter = filter_
        self.parser: MessageParser = parser
        self.repository: MessageRepository = repository

    async def run(self) -> None:
        logger.debug("start running")
        while True:
            try:
                logger.debug("goto receive")
                msg = await self.source.receive()
            except StopAsyncIteration:
                logger.debug("message source exhausted")
                break
            if not self.filter_.is_match(msg):
                continue
            else:
                logger.debug("filtered")

            parsed = self.parser.parse(msg)
            if not parsed:
                logger.debug("not parsed")
                continue
            else:
                logger.debug("parsed")

            logger.debug("saving to repo")
            await self.repository.save(parsed)
