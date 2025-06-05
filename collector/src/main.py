from __future__ import annotations

import asyncio
import shutil
from collections.abc import Awaitable, Callable
from functools import wraps

from loguru import logger
from rich.console import Console
from rich.logging import RichHandler
from twitchAPI.chat import EventData

from config import settings
from infra.filters.name_filter import NameMessageFilter
from infra.parsers.regex_parser import RegexParser
from infra.repository.mock_repository import MockRepository
from infra.twitch.twitch_auth import authenticate
from infra.twitch.twitch_client import TwichClient
from infra.twitch.twitch_source import TwitchMessageSource
from processor import MessageProcessor


def on_ready(target_channel: str) -> Callable[[EventData], Awaitable[None]]:
    @wraps(on_ready)
    async def wrapped(ready_event: EventData) -> None:
        logger.debug("Bot is ready for work, joining channels")
        await ready_event.chat.join_room(target_channel)
        logger.info(f"joined to [bold magenta]{target_channel}[/]")

    return wrapped


async def main() -> None:
    terminal_width = shutil.get_terminal_size((220, 20)).columns
    logger.configure(
        handlers=[
            {
                "sink": RichHandler(
                    console=Console(force_terminal=True, width=terminal_width),
                    markup=True,
                    rich_tracebacks=True,
                ),
                "format": "{message}",
            }
        ]
    )
    logger.debug("Starting bot")
    twitch = await authenticate(settings)

    logger.debug("Creating chat")
    client = TwichClient(twitch)
    twitch_source = TwitchMessageSource(client)
    name_filter = NameMessageFilter(["gloria_bot", "nikmosi"])
    repository = MockRepository()

    client.add_on_ready_handler(on_ready(settings.target_channels))

    processor = MessageProcessor(
        twitch_source,
        name_filter,
        RegexParser(),
        repository,
    )

    await client.start()
    logger.info("Chat created")

    try:
        logger.debug("[bold red]press Ctrl-C to stop...[/]")
        await processor.run()
    finally:
        logger.debug("[bold red]closing resources[/]")
        client.stop()
        await twitch.close()  # type: ignore[no-untyped-call]
        logger.info("closed resources")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("got Ctrl-C")
