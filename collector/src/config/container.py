from __future__ import annotations

import contextlib
from collections.abc import AsyncGenerator
from typing import cast

from dependency_injector import containers, providers
from dependency_injector.providers import Resource, Singleton
from loguru import logger
from twitchAPI.twitch import Twitch

from config.settings import Settings
from db.database import DataBase
from domain.message_filter import MessageFilter
from domain.message_parser import MessageParser
from domain.message_source import MessageSource
from domain.repository import MessageRepository
from infra.filters.name_filter import NameMessageFilter
from infra.parsers.regex_parser import RegexParser
from infra.repository.postgres import PostgresRepository
from infra.twitch.twitch_auth import authenticate
from infra.twitch.twitch_client import TwichClient
from infra.twitch.twitch_source import TwitchMessageSource


@contextlib.asynccontextmanager
async def _init_twitch(settings: Settings) -> AsyncGenerator[Twitch, None]:
    logger.debug("initing twitch")
    twitch = await authenticate(settings)
    logger.info("inited twitch")
    try:
        yield twitch
    finally:
        await twitch.close()


@contextlib.asynccontextmanager
async def _init_twitch_client(
    twitch: Twitch, settings: Settings
) -> AsyncGenerator[TwichClient, None]:
    logger.debug("Creating chat")
    client = TwichClient(twitch, settings.target_channels)
    await client.start()
    logger.info("Created chat")
    try:
        yield client
    finally:
        client.stop()


async def _init_database(settings: Settings) -> DataBase:
    return DataBase(settings.database.encoded_string())


class Container(containers.DeclarativeContainer):
    settings: Singleton[Settings] = providers.Singleton(Settings)

    twitch = providers.Resource(_init_twitch, settings=settings)

    twitch_client: Resource[TwichClient] = cast(
        Resource[TwichClient], providers.Resource(_init_twitch_client, twitch, settings)
    )
    message_source: Singleton[MessageSource] = providers.Singleton(
        TwitchMessageSource, twitch_client
    )

    name_filter: Singleton[MessageFilter] = providers.Singleton(
        NameMessageFilter, settings.provided.filtered_name
    )

    parser: Singleton[MessageParser] = providers.Singleton(RegexParser)

    database: Resource[DataBase] = providers.Resource(_init_database, settings)

    repository: Singleton[MessageRepository] = providers.Singleton(
        PostgresRepository, database
    )
