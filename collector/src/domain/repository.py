from abc import ABC, abstractmethod

from domain.values import ParsedMessage


class MessageRepository(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    async def save(self, msg: ParsedMessage) -> None:
        pass
