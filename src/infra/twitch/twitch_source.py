from __future__ import annotations

from asyncio import Queue
from typing import override

from loguru import logger
from twitchAPI.chat import ChatMessage

from domain import MessageSource
from domain.models import RawMessage
from infra.twitch.twitch_client import TwichClient
from infra.twitch.twitch_converter import convert_message


class TwitchMessageSource(MessageSource):
    def __init__(self, twitch_client: TwichClient) -> None:
        self._queue: Queue[ChatMessage] = Queue()
        twitch_client.add_message_handler(self.on_message)

    async def on_message(self, msg: ChatMessage) -> None:
        name = msg.room if msg.room is None else msg.room.name
        logger.info(
            f"in [bold magenta]{name}[/], [bold yellow]{msg.user.name}[/] said:"
            f" {msg.text}"
        )
        self._queue.put_nowait(msg)

    @override
    async def receive(self) -> RawMessage:
        msg = await self._queue.get()
        return convert_message(msg)
