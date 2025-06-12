from datetime import datetime

from twitchAPI.chat import ChatMessage

from domain.values import RawMessage


def convert_message(msg: ChatMessage) -> RawMessage:
    res = RawMessage(text=msg.text, author=msg.user.name, date=datetime.now())
    return res
