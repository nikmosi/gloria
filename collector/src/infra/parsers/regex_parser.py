import re

from domain.values import ParsedMessage, Rank, RawMessage
from logic.messages.parser import MessageParser


class RegexParser(MessageParser):
    pattern: re.Pattern[str] = re.compile(
        r"(?P<nikname>\w+),\sу вас\s"
        r"(?P<points>[\d\s]+)\sочков опыта, провел\(а\) на стримах\s"
        r"(?P<hours>[\d\s,]+)\sчасов\. В топе\s(?P<top>\d+), ты\s"
        r"(?P<rankname>\w+)\[(?P<rankposition>\d+)/(?P<totalrank>\d+)\]"
    )

    def parse(self, msg: RawMessage) -> ParsedMessage | None:
        match = self.pattern.search(msg.text)

        if not match:
            return None

        data = match.groupdict()

        return ParsedMessage(
            date=msg.date,
            nickname=data["nikname"],
            points=int(data["points"].replace(" ", "")),
            hours=float(data["hours"].replace(" ", "").replace(",", ".")),
            position=int(data["top"]),
            rank=Rank(
                name=data["rankname"],
                left=int(data["rankposition"]),
                right=int(data["totalrank"]),
            ),
        )
