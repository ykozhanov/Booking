from sqlalchemy import ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from src.db import Base


class Reservation(Base):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_name: Mapped[str]
    reservation_time: Mapped[datetime]
    duration_minutes: Mapped[int] = mapped_column(CheckConstraint("duration_minutes > 0"))

    table_id: Mapped[int] = mapped_column(ForeignKey("tables.id"))
