import re
from abc import ABC, abstractmethod

from models.Statistic import StatisticMessage


class StaticticParser(ABC):
    @abstractmethod
    def parse(self, msg: str) -> StatisticMessage | None: ...


class RegexParser(StaticticParser):
    # TODO: implement methods
    pattern: re.Pattern[str] = re.compile(
        r"-\s(?P<date>\d{2}:\d{2})\sgloria_bot:\s(?P<nikname>\w+),\sу вас\s"
        r"(?P<points>[\d\s]+)\sочков опыта, провел\(а\) на стримах\s"
        r"(?P<hours>[\d\s,]+)\sчасов\. В топе\s(?P<top>\d+), ты\s"
        r"(?P<rankname>\w+)\[(?P<rankposition>\d+)/(?P<totalrank>\d+)\]"
    )

    def parse(self, msg: str) -> StatisticMessage | None:
        pass
