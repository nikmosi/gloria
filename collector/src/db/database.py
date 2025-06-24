from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from loguru import logger
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


class DataBase:
    def __init__(self, db_url: str) -> None:
        self.db_url = db_url
        self.engine: AsyncEngine = create_async_engine(db_url)
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            autoflush=False,
            expire_on_commit=False,
        )

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        session: AsyncSession = self.session_factory()
        try:
            yield session
        except Exception as e:
            await session.rollback()
            logger.warning("got error in session context. rollback changes.")
            logger.error(e)
        finally:
            await session.aclose()
