from sqlalchemy.orm import Mapped, mapped_column
from src.db import Base


class Table(Base):
    __tablename__ = "tables"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    seats: Mapped[int]
    location: Mapped[str]
