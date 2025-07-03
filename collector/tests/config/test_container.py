# type: ignore
from unittest.mock import MagicMock

import pytest
from dependency_injector.providers import Resource, Singleton

from config.container import Container
from config.settings import Settings


class AsyncContextManagerMock:
    async def __aenter__(self):
        return MagicMock()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass


@pytest.fixture
def test_settings() -> Settings:
    # Provide minimal test Settings instance, adjust as per your Settings init
    return Settings(
        database="postgresql+asyncpg://user:123@postgres:5432/collector",
        target_channels="#testchannel",
        filtered_name=["testname"],
    )


@pytest.mark.asyncio
async def test_container_basic_init(test_settings: Settings):
    container = Container()

    # Override settings with test settings
    container.settings.override(Singleton(lambda: test_settings))

    container.twitch.override(Resource(lambda: AsyncContextManagerMock()))

    # Override twitch_client resource similarly
    container.twitch_client.override(Resource(lambda: AsyncContextManagerMock()))

    # Await database resource (no async context manager in your code)
    db = await container.database()
    assert db is not None

    # Test singleton providers can be created and injected correctly
    message_source = container.message_source()
    assert message_source is not None

    name_filter = container.name_filter()
    assert name_filter is not None

    parser = container.parser()
    assert parser is not None

    repository = container.repository()
    assert repository is not None

    processor = container.processor()
    assert processor is not None


@pytest.mark.asyncio
async def test_processor_with_mocks(test_settings: Settings):
    container = Container()
    container.settings.override(Singleton(lambda: test_settings))

    # Create mocks
    mock_source = MagicMock()
    mock_filter = MagicMock()
    mock_parser = MagicMock()
    mock_repo = MagicMock()

    # Override dependencies with mocks
    container.message_source.override(Singleton(lambda: mock_source))
    container.name_filter.override(Singleton(lambda: mock_filter))
    container.parser.override(Singleton(lambda: mock_parser))
    container.repository.override(Singleton(lambda: mock_repo))

    # Instantiate processor, injected with mocks
    processor = container.processor()
    assert processor.source is mock_source
    assert processor.filter_ is mock_filter
    assert processor.parser is mock_parser
    assert processor.repository is mock_repo
