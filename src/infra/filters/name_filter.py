from collections.abc import Iterable

from twitchAPI.chat import ChatMessage

from domain import MessageFilter


class NameMessageFilter(MessageFilter):
    def __init__(self, name: Iterable[str]) -> None:
        self.name = name

    def is_match(self, msg: ChatMessage) -> bool:
        return msg.user.name in self.name
