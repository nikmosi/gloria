from sqlalchemy.dialects.postgresql import insert as pg_insert

from db.database import DataBase
from db.models.base import HistoryMessage, LastMessage
from domain.repository import MessageRepository
from domain.values.statistic import ParsedMessage


class PostgresRepository(MessageRepository):
    def __init__(self, database: DataBase) -> None:
        self.database = database
        super().__init__()

    async def save(self, msg: ParsedMessage) -> None:
        async with self.database.session() as s:
            stmt = (
                pg_insert(LastMessage)
                .values(
                    nickname=msg.nickname,
                    date=msg.date,
                    points=msg.points,
                    hours=msg.hours,
                    position=msg.position,
                    rank_name=msg.rank.name,
                    rank_left=msg.rank.left,
                    rank_right=msg.rank.right,
                )
                .on_conflict_do_update(
                    index_elements=["nickname"],  # поле с уникальным ограничением / PK
                    set_={
                        "date": msg.date,
                        "points": msg.points,
                        "hours": msg.hours,
                        "position": msg.position,
                        "rank_name": msg.rank.name,
                        "rank_left": msg.rank.left,
                        "rank_right": msg.rank.right,
                    },
                )
            )

            history_msg = HistoryMessage(
                nickname=msg.nickname,
                date=msg.date,
                points=msg.points,
                hours=msg.hours,
                position=msg.position,
                rank_name=msg.rank.name,
                rank_left=msg.rank.left,
                rank_right=msg.rank.right,
            )
            await s.execute(stmt)
            s.add(history_msg)
            await s.commit()
