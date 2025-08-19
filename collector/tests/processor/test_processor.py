from datetime import datetime

import pytest

from domain.values.message import RawMessage
from domain.values.statistic import ParsedMessage, Rank
from infra.repository.fake import FakeRepository
from infra.source.fake import FakeMessageSource
from logic.messages.filter import MessageFilter
from logic.messages.parser import MessageParser
from logic.processor import MessageProcessor


class AllowAllFilter(MessageFilter):
    def is_match(self, msg: RawMessage) -> bool:  # noqa: D401
        """Return True for any message."""
        return True


class EchoParser(MessageParser):
    def parse(self, msg: RawMessage) -> ParsedMessage | None:  # noqa: D401
        """Convert RawMessage to ParsedMessage with dummy data."""
        return ParsedMessage(
            date=msg.date,
            nickname=msg.author,
            points=0,
            hours=0.0,
            position=0,
            rank=Rank(name="", left=0, right=0),
        )


@pytest.mark.asyncio
async def test_processor_exits_when_source_exhausted() -> None:
    messages = [
        RawMessage(text=f"msg {i}", author="user", date=datetime.now())
        for i in range(3)
    ]
    repository = FakeRepository()
    processor = MessageProcessor(
        FakeMessageSource(messages),
        AllowAllFilter(),
        EchoParser(),
        repository,
    )

    await processor.run()

    assert len(repository.get_saved()) == len(messages)


@pytest.mark.asyncio
async def test_processor_exits_on_empty_source() -> None:
    repository = FakeRepository()
    processor = MessageProcessor(
        FakeMessageSource([]),
        AllowAllFilter(),
        EchoParser(),
        repository,
    )

    await processor.run()

    assert repository.get_saved() == []
