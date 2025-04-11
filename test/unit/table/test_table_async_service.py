import pytest
from unittest.mock import AsyncMock
from src.services import TableAsyncService
from src.repositories import SQLAlchemyAsyncTableRepository
from src.schemas import TableCreateSchema, TableResponseSchema
from src.exceptions import TableDeletedException


@pytest.mark.asyncio
async def test_create_table_success():
    """Тест успешного создания столика."""

    mock_repo = AsyncMock(spec=SQLAlchemyAsyncTableRepository)
    service = TableAsyncService(mock_repo)

    table_data = TableCreateSchema(
        name="Стол 1",
        seats=1,
        location="У окна",
    )

    mock_repo.create.return_value = TableResponseSchema(
        id=1,
        name=table_data.name,
        seats=table_data.seats,
        location=table_data.location,
    )

    table = await service.create_table(table_data)

    assert table.name == "Стол 1"
    assert table.seats == 1


@pytest.mark.asyncio
async def test_delete_table_has_reservations():
    """Тест на ошибку удаления стола с бронью."""

    mock_repo = AsyncMock(spec=SQLAlchemyAsyncTableRepository)
    service = TableAsyncService(mock_repo)

    mock_repo.delete.side_effect = TableDeletedException()

    table_data = TableCreateSchema(
        name="Стол 1",
        seats=1,
        location="У окна",
    )

    with pytest.raises(TableDeletedException):
        await service.delete_table(table_data)
