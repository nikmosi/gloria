from domain.message_filter import MessageFilter
from domain.message_parser import MessageParser
from domain.message_source import MessageSource
from domain.repository import MessageRepository


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
        while True:
            msg = await self.source.receive()
            if not self.filter_.is_match(msg):
                continue

            parsed = self.parser.parse(msg)
            if not parsed:
                continue

            self.repository.save(parsed)
