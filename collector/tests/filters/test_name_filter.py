from datetime import datetime

from domain.values.message import RawMessage
from infra.filters.name_filter import NameMessageFilter


def test_name_filter_matches() -> None:
    msg_filter = NameMessageFilter(["bot", "alice"])
    msg = RawMessage(text="hello", author="bot", date=datetime.now())
    assert msg_filter.is_match(msg) is True


def test_name_filter_rejects_other_users() -> None:
    msg_filter = NameMessageFilter(["bot", "alice"])
    msg = RawMessage(text="random viewer text", author="bob", date=datetime.now())
    assert msg_filter.is_match(msg) is False
