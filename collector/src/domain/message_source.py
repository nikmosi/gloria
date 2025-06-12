from abc import ABC, abstractmethod

from domain.values import RawMessage


class MessageSource(ABC):
    @abstractmethod
    async def receive(self) -> RawMessage:
        pass
