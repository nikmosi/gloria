import pytest
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import Base


class FakeUser(Base):
    __tablename__ = "fake_users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    age: Mapped[int] = mapped_column(Integer)


@pytest.fixture
def user_instance() -> FakeUser:
    return FakeUser(id=1, username="nikmosi", age=30)


def test_to_dict(user_instance: FakeUser) -> None:
    result = user_instance.to_dict()
    assert result == {"id": 1, "username": "nikmosi", "age": 30}
