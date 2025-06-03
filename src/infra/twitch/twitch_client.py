from collections.abc import Awaitable, Callable

from twitchAPI.chat import Chat, ChatEvent, ChatMessage
from twitchAPI.twitch import Twitch


class TwichClient:
    def __init__(self, twitch: Twitch) -> None:
        self.chat = Chat(twitch)

    def add_message_handler(
        self, handler: Callable[[ChatMessage], Awaitable[None]]
    ) -> None:
        self.chat.register_event(ChatEvent.MESSAGE, handler)

    def add_on_ready_handler(
        self, handler: Callable[[ChatMessage], Awaitable[None]]
    ) -> None:
        self.chat.register_event(ChatEvent.READY, handler)

    async def start(self) -> None:
        await self.chat
        self.chat.start()

    def stop(self) -> None:
        self.chat.stop()
