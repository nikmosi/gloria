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
        logger.info("Message processor started")
        while True:
            try:
                msg = await self.source.receive()
            except StopAsyncIteration:
                logger.info("Message source exhausted, processor stopping")
                break

            if not self.filter_.is_match(msg):
                continue

            logger.info(f"Received target message from '{msg.author}': {msg.text}")

            parsed = self.parser.parse(msg)
            if not parsed:
                logger.warning(
                    f"Failed to parse target message from '{msg.author}': {msg.text}"
                )
                continue

            await self.repository.save(parsed)
            logger.info(
                f"Saved stats for '{parsed.nickname}': {parsed.points} points, "
                f"{parsed.hours}h, rank '{parsed.rank.name}'"
            )
