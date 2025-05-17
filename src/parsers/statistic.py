import re
from abc import ABC, abstractmethod

from models.message import Message
from models.statistic import StatisticMessage


class StaticticParser(ABC):
    @abstractmethod
    def parse(self, msg: Message) -> StatisticMessage | None: ...


class RegexParser(StaticticParser):
    # TODO: implement methods
    pattern: re.Pattern[str] = re.compile(
        r"(?P<nikname>\w+),\sу вас\s"
        r"(?P<points>[\d\s]+)\sочков опыта, провел\(а\) на стримах\s"
        r"(?P<hours>[\d\s,]+)\sчасов\. В топе\s(?P<top>\d+), ты\s"
        r"(?P<rankname>\w+)\[(?P<rankposition>\d+)/(?P<totalrank>\d+)\]"
    )

    def parse(self, msg: Message) -> StatisticMessage | None:
        pass
