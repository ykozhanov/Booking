from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models import Table
from src.exceptions import TableNotFoundException
from src.schemas import TableCreateSchema, TableUpdateSchema


class TableAsyncRepositoryInterface(ABC):
    @abstractmethod
    async def create(self, table: TableCreateSchema) -> Table:
        """Добавить новый столик. Возвращает объект Table."""
        pass

    @abstractmethod
    async def get_by_id(self, table_id: int) -> Table:
        """Найти столик по ID. Выбрасывает исключение TableNotFoundException если не найден."""
        pass

    @abstractmethod
    async def get_all(self) -> list[Table]:
        """Получить все столики."""
        pass

    @abstractmethod
    async def delete(self, table_id: int) -> None:
        """Удалить столик по ID."""
        pass

    @abstractmethod
    async def update(self, update_table: TableUpdateSchema) -> Table:
        """Обновить столик. Возвращает обновленный объект Table."""
        pass


class SQLAlchemyAsyncTableRepository(TableAsyncRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, table: TableCreateSchema) -> Table:
        new_table = Table(name=table.name, seats=table.seats, location=table.location)
        self.session.add(new_table)
        await self.session.commit()
        return new_table

    async def get_by_id(self, table_id: int) -> Table:
        result = await self.session.execute(select(Table).filter(Table.id == table_id))
        table = result.scalars().first()
        if not table:
            raise TableNotFoundException()
        return table

    async def get_all(self) -> list[Table]:
        result = await self.session.execute(select(Table))
        tables = list(result.scalars().all())
        return tables


    async def delete(self, table_id: int) -> None:
        table = await self.get_by_id(table_id)
        await self.session.delete(table)
        await self.session.commit()

    async def update(self, update_table: TableUpdateSchema) -> Table:
        table = await self.get_by_id(update_table.id)

        if update_table.name:
            table.name = update_table.name
        if update_table.seats:
            table.seats = update_table.seats
        if update_table.location:
            table.location = update_table.location

        await self.session.commit()
        return table
