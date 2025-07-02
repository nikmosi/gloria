from collections.abc import Iterable
from typing import override

from domain.values.message import RawMessage
from logic.messages.source import MessageSource


class FakeMessageSource(MessageSource):
    def __init__(self, messages: Iterable[RawMessage]) -> None:
        self._messages = iter(messages)
        super().__init__()

    @override
    async def receive(self) -> RawMessage:
        try:
            return next(self._messages)
        except StopIteration as e:
            raise StopAsyncIteration from e
