from abc import ABC, abstractmethod

from twitchAPI.chat import ChatMessage


class MessageFilter(ABC):
    @abstractmethod
    def is_match(self, msg: ChatMessage) -> bool:
        pass
