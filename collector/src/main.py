from __future__ import annotations

import asyncio

from dependency_injector.wiring import Provide, inject
from loguru import logger

from config.container import Container
from config.init import init_container
from domain.message_filter import MessageFilter
from domain.message_parser import MessageParser
from domain.message_source import MessageSource
from domain.repository import MessageRepository
from infra.logging.logging import setup_logger
from logic.processor import MessageProcessor


@inject
async def main(
    twitch_source: MessageSource = Provide[Container.message_source],
    name_filter: MessageFilter = Provide[Container.name_filter],
    parser: MessageParser = Provide[Container.parser],
    repository: MessageRepository = Provide[Container.repository],
) -> None:
    processor = MessageProcessor(
        twitch_source,
        name_filter,
        parser,
        repository,
    )

    try:
        logger.debug("[bold red]press Ctrl-C to stop...[/]")
        await processor.run()
    finally:
        logger.debug("[bold red]exit[/]")


async def middleware():
    setup_logger()
    container = await init_container()
    container.wire(modules=[__name__])
    await main()


if __name__ == "__main__":
    try:
        asyncio.run(middleware())
    except KeyboardInterrupt:
        logger.info("got Ctrl-C")
