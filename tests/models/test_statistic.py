from datetime import datetime

from domain.models import ParsedMessage, Rank


def test_static_message():
    date: datetime = datetime.now()
    nickname: str = "nikmosi"
    points: int = 10
    hours: float = 0.1
    position: int = 20
    rank: Rank = Rank(name="bob", left=11, right=20)

    message = ParsedMessage(
        date=date,
        nickname=nickname,
        points=points,
        hours=hours,
        position=position,
        rank=rank,
    )

    assert message.date == date
    assert message.nickname == nickname
    assert message.points == points
    assert message.hours == hours
    assert message.position == position
    assert message.rank == rank


def test_rank():
    name = "bob"
    left = 11
    right = 20

    rank = Rank(name=name, left=left, right=right)

    assert rank.name == name
    assert rank.left == left
    assert rank.right == right
