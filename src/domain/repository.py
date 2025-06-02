from abc import ABC, abstractmethod

from domain.models import ParsedMessage


class MessageRepository(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def save(self, msg: ParsedMessage) -> None:
        pass
