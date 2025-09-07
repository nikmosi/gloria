from collections.abc import Awaitable, Callable

from loguru import logger
from twitchAPI.chat import Chat, ChatEvent, ChatMessage, EventData
from twitchAPI.twitch import Twitch


class TwichClient:
    def __init__(self, twitch: Twitch, target_channels: list[str] | str) -> None:
        self.targets = target_channels
        self.chat = Chat(twitch)
        self.add_on_ready_handler(self._on_ready)

    def add_message_handler(
        self, handler: Callable[[ChatMessage], Awaitable[None]]
    ) -> None:
        logger.debug("add_message_handler")
        self.chat.register_event(ChatEvent.MESSAGE, handler)

    def add_on_ready_handler(
        self, handler: Callable[[ChatMessage], Awaitable[None]]
    ) -> None:
        logger.debug("add_ready_handler")
        self.chat.register_event(ChatEvent.READY, handler)

    async def start(self) -> None:
        logger.debug("start")
        await self.chat
        self.chat.start()

    def stop(self) -> None:
        self.chat.stop()

    async def _on_ready(self, ready_event: EventData) -> None:
        logger.debug("Bot is ready for work, joining channels")
        await ready_event.chat.join_room(self.targets)
        logger.info(
            f"joined to [bold magenta]{self.targets}[/] as {ready_event.chat.username}"
        )
