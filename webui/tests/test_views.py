from __future__ import annotations

from datetime import datetime
import re

import pytest
from litestar.testing import TestClient
from pony.orm import db_session

from src.config.settings import Database, Settings
from src.db.models import Message
from src.main import create_app


def _seed() -> None:
    with db_session:
        Message(
            nickname="alice",
            date=datetime(2024, 1, 1, 12, 0),
            points=10,
            hours=1.0,
            position=1,
            rank_name="First",
            rank_left=0,
            rank_right=1,
        )
        Message(
            nickname="alice",
            date=datetime(2024, 1, 2, 12, 0),
            points=15,
            hours=1.5,
            position=1,
            rank_name="Second",
            rank_left=0,
            rank_right=1,
        )
        Message(
            nickname="bob",
            date=datetime(2024, 1, 1, 11, 0),
            points=20,
            hours=2.0,
            position=2,
            rank_name="Third",
            rank_left=0,
            rank_right=1,
        )


@pytest.fixture(scope="module")
def app(tmp_path_factory):
    db_file = tmp_path_factory.mktemp("db") / "test.db"
    settings = Settings(database=Database(dsn=f"sqlite:///{db_file}"))
    return create_app(settings, create_tables=True)


@pytest.fixture(autouse=True)
def seed(app):
    with db_session:
        Message.select().delete(bulk=True)
    _seed()
    yield


@pytest.fixture()
def client(app):
    with TestClient(app) as client:
        yield client


def _rows(html: str) -> list[tuple[str, str, str, str]]:
    pattern = r"<tr>\s*<td>([^<]+)</td>\s*<td>([^<]+)</td>\s*<td>([^<]+)</td>\s*<td>([^<]+)</td>\s*</tr>"
    return re.findall(pattern, html)


def test_home_renders_table(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "<table" in response.text


def test_sorting_default(client: TestClient) -> None:
    response = client.get("/partials/messages-table")
    rows = _rows(response.text)
    assert [r[0] for r in rows] == ["1", "1", "2"]
    assert rows[0][1] > rows[1][1]


def test_pagination(client: TestClient) -> None:
    response = client.get("/partials/messages-table", params={"page": 2, "page_size": 1})
    rows = _rows(response.text)
    assert len(rows) == 1
    assert rows[0][0] == "1" and "2024-01-01" in rows[0][1]
