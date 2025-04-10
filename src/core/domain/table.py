from dataclasses import dataclass
from src.core.exceptions import ValidationException

@dataclass
class Table:
    id: int | None
    name: str
    seats: int
    location: str

    def __post_init__(self):
        self._validate()

    def _validate(self) -> None:
            """Валидация данных"""
            if self.seats <= 0:
                raise ValidationException("Количество мест должно быть положительным")
