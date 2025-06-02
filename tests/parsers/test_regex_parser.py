import datetime

from domain.models import RawMessage
from infra.parsers import RegexParser


def test_regex_parser():
    text = (
        "nikmosi, у вас 329234 очков опыта, провел(а) "
        "на стримах 2 594,75 часов. В топе 10, ты боб[12/20]."
    )
    msg = RawMessage(text=text, date=datetime.datetime.now())

    parser = RegexParser()
    result = parser.parse(msg)

    assert result is not None
    assert result.nickname == "nikmosi"
    assert result.points == 329234
    assert result.hours == 2594.75
    assert result.position == 10
    assert result.rank.name == "боб"
    assert result.rank.left == 12
    assert result.rank.right == 20
