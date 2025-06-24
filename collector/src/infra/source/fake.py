from collections.abc import Iterable
from typing import override

from domain.message_source import MessageSource
from domain.values.message import RawMessage


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
