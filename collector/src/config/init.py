from collections.abc import Awaitable
from functools import lru_cache

from dependency_injector.containers import DeclarativeContainer

from .container import Container


@lru_cache(1)
async def init_container() -> Container:
    con = await _create_container()
    await _init_container(con)
    return con


async def _create_container() -> Container:
    container = Container()
    return container


async def _init_container(container: DeclarativeContainer) -> None:
    to_await = container.init_resources()
    if isinstance(to_await, Awaitable):
        await to_await
