from abc import ABC, abstractmethod

from domain.models import ParsedMessage, RawMessage


class MessageParser(ABC):
    @abstractmethod
    def parse(self, msg: RawMessage) -> ParsedMessage | None:
        pass
