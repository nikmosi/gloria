from datetime import datetime

import pytest

from domain.values.statistic import ParsedMessage, Rank
from infra.repository.fake import FakeRepository


@pytest.fixture
def repository() -> FakeRepository:
    return FakeRepository()


@pytest.mark.asyncio
async def test_fake_repository(repository: FakeRepository):
    assert repository.get_saved().__len__() == 0

    msg = ParsedMessage(
        date=datetime.now(),
        nickname="wow",
        points=1000,
        hours=100,
        position=10,
        rank=Rank(name="bo", left=1, right=29),
    )

    await repository.save(msg)

    assert repository.get_saved().__len__() == 1

    await repository.save(msg)
    await repository.save(msg)
    await repository.save(msg)

    assert repository.get_saved().__len__() == 4
