from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models import Table, Reservation
from src.exceptions import TableNotFoundException, DeletedException
from src.schemas import TableCreateSchema, TableUpdateSchema


class TableRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, table: TableCreateSchema) -> Table:
        """Добавить новый стол. Возвращает объект Table."""
        new_table = Table(name=table.name, seats=table.seats, location=table.location)
        self.session.add(new_table)
        await self.session.commit()
        return new_table

    async def get_by_id(self, table_id: int) -> Table:
        """Найти столик по ID. Выбрасывает исключение TableNotFoundException если не найден."""
        result = await self.session.execute(select(Table).filter(Table.id == table_id))
        table = result.scalars().first()
        if not table:
            raise TableNotFoundException()
        return table

    async def get_all(self) -> list[Table]:
        """Получить все столики."""
        result = await self.session.execute(select(Table))
        tables = list(result.scalars().all())
        return tables

    async def _check_table_has_reservations(self, table_id: int) -> None:
        """Проверка на наличие брони у столика. Если столик имеет бронь, выбросит исключение DeletedException."""
        reservations = await self.session.execute(
            select(Reservation).filter(Reservation.table_id == table_id)
        )
        if reservations:
            raise DeletedException("Нельзя удалить стол пока у него есть бронь.")

    async def delete(self, table_id: int) -> None:
        """Удалить столик по ID."""
        table = await self.get_by_id(table_id)
        await self._check_table_has_reservations(table_id)
        await self.session.delete(table)
        await self.session.commit()

    async def update(self, update_table: TableUpdateSchema) -> Table:
        """Обновить столик. Возвращает обновленный объект Table."""
        table = await self.get_by_id(update_table.id)

        if update_table.name:
            table.name = update_table.name
        if update_table.seats:
            table.seats = update_table.seats
        if update_table.location:
            table.location = update_table.location

        await self.session.commit()
        return table
