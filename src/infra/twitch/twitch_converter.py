from datetime import datetime

from twitchAPI.chat import ChatMessage

from domain.models import RawMessage


def convert_message(msg: ChatMessage) -> RawMessage:
    sent_date = datetime.fromtimestamp(msg.sent_timestamp)
    return RawMessage(text=msg.text, date=sent_date, author=msg.user.name)
