from __future__ import annotations

import asyncio
from asyncio import Queue
from typing import override

from loguru import logger
from twitchAPI.chat import ChatMessage

from domain.values import RawMessage
from infra.twitch.twitch_client import TwichClient
from infra.twitch.twitch_converter import convert_message
from logic.messages.source import MessageSource


class TwitchMessageSource(MessageSource):
    def __init__(self, twitch_client: TwichClient) -> None:
        self._queue: Queue[ChatMessage] = Queue()
        self._main_loop = asyncio.get_running_loop()

        twitch_client.add_message_handler(self.on_message)

    async def _put_message(self, msg: ChatMessage) -> None:
        room = msg.room
        name = "None" if room is None else room.name

        logger.info(
            f"in [bold magenta]{name}[/], [bold yellow]{msg.user.name}[/] said:"
            f" {msg.text}"
        )
        await self._queue.put(msg)

    async def on_message(self, msg: ChatMessage) -> None:
        asyncio.run_coroutine_threadsafe(self._put_message(msg), self._main_loop)

    @override
    async def receive(self) -> RawMessage:
        msg = await self._queue.get()
        return convert_message(msg)
