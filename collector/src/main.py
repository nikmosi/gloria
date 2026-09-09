from __future__ import annotations

import asyncio
import contextlib

from dependency_injector.wiring import Provide, inject
from loguru import logger

from config.container import Container
from config.init import init_container
from logic.processor import MessageProcessor


@inject
async def main(processor: MessageProcessor = Provide[Container.processor]) -> None:
    try:
        logger.info("Starting collector service")
        await processor.run()
    finally:
        logger.info("Collector service finished")


async def wire_container() -> None:
    container = await init_container()
    container.wire(modules=[__name__])
    await main()


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt):
        asyncio.run(wire_container())
