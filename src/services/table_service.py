from src.repositories import (
    TableAsyncRepositoryInterface,
    ReservationAsyncRepositoryInterface,
)
from src.schemas import TableCreateSchema, TableUpdateSchema, TableResponseSchema
from src.exceptions import TableDeletedException


class TableAsyncService:
    def __init__(
        self,
        table_repository: TableAsyncRepositoryInterface,
        reservation_repository: ReservationAsyncRepositoryInterface,
    ):
        self.table_repository = table_repository
        self.reservation_repository = reservation_repository

    async def get_all_tables(self) -> list[TableResponseSchema]:
        """Получить список всех столиков."""
        tables = await self.table_repository.get_all()
        return [TableResponseSchema.model_validate(t) for t in tables]

    async def create_table(self, table: TableCreateSchema) -> TableResponseSchema:
        """Создать новый столик."""
        new_table = await self.table_repository.create(table)
        return TableResponseSchema.model_validate(new_table)

    async def _check_table_has_reservations(self, table_id: int) -> None:
        """Проверка на наличие брони у столика. Если столик имеет бронь, выбросит исключение DeletedException."""
        reservations = await self.reservation_repository.get_by_table_id(table_id)
        if reservations:
            raise TableDeletedException("Нельзя удалить стол пока у него есть бронь")

    async def delete_table(self, table_id: int) -> None:
        """Удалить столик по ID."""
        await self._check_table_has_reservations(table_id)
        await self.table_repository.delete(table_id)

    async def update_table(
        self, update_table: TableUpdateSchema
    ) -> TableResponseSchema:
        """Обновить столик."""
        updated_table = await self.table_repository.update(update_table)
        return TableResponseSchema.model_validate(updated_table)
