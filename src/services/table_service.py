from src.repositories import TableRepository
from src.schemas import TableCreateSchema, TableUpdateSchema, TableResponseSchema


class TableService:
    def __init__(self, table_repository: TableRepository):
        self.table_repository = table_repository

    async def get_all_tables(self) -> list[TableResponseSchema]:
        """Получить список всех столиков."""
        tables = await self.table_repository.get_all()
        return [TableResponseSchema.model_validate(t) for t in tables]

    async def create_table(self, table: TableCreateSchema) -> TableResponseSchema:
        """Создать новый столик."""
        new_table = await self.table_repository.create(table)
        return TableResponseSchema.model_validate(new_table)

    async def delete_table(self, table_id: int) -> None:
        """Удалить столик по ID."""
        await self.table_repository.delete(table_id)

    async def update_table(
        self, update_table: TableUpdateSchema
    ) -> TableResponseSchema:
        """Обновить столик."""
        updated_table = await self.table_repository.update(update_table)
        return TableResponseSchema.model_validate(updated_table)
