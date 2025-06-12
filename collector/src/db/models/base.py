from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True


class LastMessage(Base):
    __tablename__ = "last_messages"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
