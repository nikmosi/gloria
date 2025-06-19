from collections.abc import Awaitable
from functools import lru_cache

from dependency_injector.containers import DeclarativeContainer

from .container import Container


@lru_cache(1)
async def init_container() -> DeclarativeContainer:
    return await _init_container()


async def _init_container() -> DeclarativeContainer:
    container = Container()
    to_await = container.init_resources()
    if isinstance(to_await, Awaitable):
        await to_await

    return container
