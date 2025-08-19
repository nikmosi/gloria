# type: ignore
import pytest
from sqlalchemy import text

from db.database import DataBase


@pytest.fixture
def db() -> DataBase:
    return DataBase("sqlite+aiosqlite:///:memory:")


@pytest.mark.asyncio
async def test_session_rollback_on_exception(db: DataBase):
    class CustomError(Exception):
        pass

    # Создаём таблицу вручную, чтобы всё было в одном тесте
    async with db.session() as session:
        await session.execute(
            text("""
            CREATE TABLE items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT
            )
        """)
        )

    # Пытаемся добавить запись и вызвать ошибку
    with pytest.raises(CustomError):
        async with db.session() as session:
            await session.execute(text("INSERT INTO items (name) VALUES ('test')"))
            result = await session.execute(text("SELECT COUNT(*) FROM items"))
            count_before = result.scalar()
            assert count_before == 1  # запись добавлена
            raise CustomError("Force rollback")

    # Проверяем, что после rollback в таблице пусто
    async with db.session() as session:
        result = await session.execute(text("SELECT COUNT(*) FROM items"))
        count_after = result.scalar()
        assert count_after == 0  # rollback сработал, записи нет
