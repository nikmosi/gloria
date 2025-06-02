from collections.abc import Awaitable, Callable

from twitchAPI.chat import Chat, ChatEvent, ChatMessage


class TwichClient:
    def __init__(self, chat: Chat) -> None:
        self.chat = chat

    def add_message_handler(self, handler: Callable[[ChatMessage], Awaitable[None]]):
        self.chat.register_event(ChatEvent.MESSAGE, handler)

    def add_on_ready_handler(self, handler: Callable[[ChatMessage], Awaitable[None]]):
        self.chat.register_event(ChatEvent.READY, handler)
