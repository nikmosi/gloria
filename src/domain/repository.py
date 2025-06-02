from abc import ABC, abstractmethod

from domain.models import ParsedMessage


class MessageRepository(ABC):
    @abstractmethod
    def save(self, msg: ParsedMessage) -> None:
        pass
