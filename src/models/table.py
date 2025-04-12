from sqlalchemy import CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column
from src.core.db import Base


class Table(Base):
    __tablename__ = "tables"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    seats: Mapped[int] = mapped_column(CheckConstraint("seats > 0"))
    location: Mapped[str]
