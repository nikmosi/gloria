import pytest
from loguru import logger

from infra.twitch.twitch_client import TwichClient


class DummyChat:
    username = "dummy_user"

    async def join_room(self, channels: str) -> None:
        self.joined = channels


class DummyReadyEvent:
    def __init__(self) -> None:
        self.chat = DummyChat()


@pytest.mark.asyncio
async def test_on_ready_logs_connected_message(caplog):
    client = object.__new__(TwichClient)
    client.targets = "#test"
    event = DummyReadyEvent()

    with caplog.at_level("DEBUG"):
        handler_id = logger.add(caplog.handler, level="DEBUG")
        await TwichClient._on_ready(client, event)
        logger.remove(handler_id)

    assert f"Connected as: {event.chat.username}" in caplog.text
