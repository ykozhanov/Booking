from abc import ABC, abstractmethod
from datetime import datetime
from src.core.domain import Reservation


class ReservationRepository(ABC):
    """Абстракция для работы с хранилищем броней"""

    @abstractmethod
    def get_by_id(self, reservation_id: int) -> Reservation:
        """Найти бронь по ID. Выбрасывает исключение ReservationNotFoundException если не найдена."""
        pass

    @abstractmethod
    def get_all_for_table(self, table_id: int) -> list[Reservation]:
        """Получить все брони для столика."""
        pass

    @abstractmethod
    def get_for_table_by_time(
        self, table_id: int, start_time: datetime, end_time: datetime
    ) -> list[Reservation]:
        """Получить все брони для столика в заданном временном промежутке."""
        pass

    @abstractmethod
    def add(self, reservation: Reservation) -> Reservation:
        """Добавить новую бронь. Возвращает объект с обновленным ID"""
        pass

    @abstractmethod
    def delete(self, reservation_id: int) -> None:
        """Удалить бронь по ID."""
        pass

    @abstractmethod
    def list_all(self) -> list[Reservation]:
        """Получить все брони."""
        pass
