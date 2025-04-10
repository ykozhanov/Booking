from dataclasses import dataclass
from datetime import datetime, timedelta
from src.core.exceptions import ValidationException


@dataclass
class Reservation:
    id: int | None
    customer_name: str
    table_id: int
    reservation_time: datetime
    duration_minutes: int

    def __post_init__(self):
        self._validate()

    def is_conflicting(self, other: "Reservation") -> bool:
        """Проверка на конфликт по времени с другим столом"""
        self_end = self.reservation_time + timedelta(minutes=self.duration_minutes)
        other_end = other.reservation_time + timedelta(minutes=other.duration_minutes)
        return (
            self.table_id == other.table_id
            and self.reservation_time < other_end
            and self_end > other.reservation_time
        )

    def _validate(self) -> None:
            """Валидация данных"""
            if self.duration_minutes <= 0:
                raise ValidationException("Длительность должна быть положительной")

            if self.reservation_time < datetime.now():
                raise ValidationException("Бронь в прошлом невозможна")
