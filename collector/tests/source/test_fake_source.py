from datetime import datetime, timedelta

import pytest
from faker import Faker

from domain.values.message import RawMessage
from infra.source.fake import FakeMessageSource


@pytest.fixture
def raw_messages(faker: Faker) -> list[RawMessage]:
    base_time = datetime.now()
    return [
        RawMessage(
            text=f"Test message #{i+1} {faker.text(max_nb_chars=100)}",
            author=f"user{i%5}",
            date=base_time - timedelta(minutes=i),
        )
        for i in range(15)
    ]


@pytest.mark.asyncio
async def test_fake_message_source(raw_messages: list[RawMessage]):
    source = FakeMessageSource(raw_messages)
    for msg in raw_messages:
        received = await source.receive()
        assert msg == received

    with pytest.raises(StopAsyncIteration):
        await source.receive()
