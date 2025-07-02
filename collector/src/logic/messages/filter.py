from abc import ABC, abstractmethod

from domain.values import RawMessage


class MessageFilter(ABC):
    @abstractmethod
    def is_match(self, msg: RawMessage) -> bool:
        pass
