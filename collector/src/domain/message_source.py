from abc import ABC, abstractmethod

from domain.models.message import RawMessage


class MessageSource(ABC):
    @abstractmethod
    async def receive(self) -> RawMessage:
        pass
