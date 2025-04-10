from abc import ABC, abstractmethod
from src.core.domain import Table


class TableRepository(ABC):
    """Абстракция для работы с хранилищем столиков"""

    @abstractmethod
    def get_by_id(self, table_id: int) -> Table:
        """Найти столик по ID. Выбрасывает исключение TableNotFoundException если не найден."""
        pass

    @abstractmethod
    def add(self, table: Table) -> Table:
        """Добавить новый столик. Возвращает объект с обновленным ID"""
        pass

    @abstractmethod
    def delete(self, table_id: int) -> None:
        """Удалить столик по ID."""
        pass

    @abstractmethod
    def list_all(self) -> list[Table]:
        """Получить все столики."""
        pass
