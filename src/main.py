from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from functools import wraps

from loguru import logger
from rich.logging import RichHandler
from twitchAPI.chat import Chat, ChatEvent, ChatMessage, EventData

from config import settings
from infra.twitch.twitch_auth import authenticate


def on_ready(target_channel: str) -> Callable[[EventData], Awaitable[None]]:
    @wraps(on_ready)
    async def wrapped(ready_event: EventData) -> None:
        logger.debug("Bot is ready for work, joining channels")
        await ready_event.chat.join_room(target_channel)
        logger.info(f"joined to [bold magenta]{target_channel}[/]")

    return wrapped


async def on_message(msg: ChatMessage):
    name = msg.room if msg.room is None else msg.room.name
    logger.info(
        f"in [bold magenta]{name}[/], [bold yellow]{msg.user.name}[/] said: {msg.text}"
    )


async def main():
    logger.configure(
        handlers=[{"sink": RichHandler(markup=True), "format": "{message}"}]
    )
    logger.debug("Starting bot")
    twitch = await authenticate(settings)

    logger.debug("Creating chat")
    chat = await Chat(twitch)
    chat.register_event(ChatEvent.READY, on_ready(settings.target_chanels))
    chat.register_event(ChatEvent.MESSAGE, on_message)
    chat.start()
    logger.info("Chat created")

    try:
        logger.debug("[bold red]press Ctrl-C to stop...[/]")
        while True:
            await asyncio.sleep(1)
    finally:
        chat.stop()
        await twitch.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("got Ctrl-C")
