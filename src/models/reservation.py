from sqlalchemy import ForeignKey, CheckConstraint
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from src.core.db import Base


class Reservation(Base):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_name: Mapped[str]
    reservation_time: Mapped[datetime] = mapped_column(type_=TIMESTAMP(timezone=True))
    duration_minutes: Mapped[int] = mapped_column(
        CheckConstraint("duration_minutes > 0")
    )

    table_id: Mapped[int] = mapped_column(ForeignKey("tables.id"))
