import pytest
from datetime import datetime, timedelta, UTC
from unittest.mock import AsyncMock
from src.services import ReservationAsyncService
from src.repositories import SQLAlchemyAsyncReservationRepository
from src.schemas import ReservationCreateSchema, ReservationResponseSchema
from src.exceptions import ReservationConflictException


@pytest.mark.asyncio
async def test_create_reservation_success():
    """Тест успешного создания брони."""

    mock_repo = AsyncMock(spec=SQLAlchemyAsyncReservationRepository)
    service = ReservationAsyncService(mock_repo)

    reservation_data = ReservationCreateSchema(
        customer_name="Алиса",
        table_id=1,
        reservation_time=datetime.now(UTC) + timedelta(days=1),
        duration_minutes=60,
    )

    mock_repo.create.return_value = ReservationResponseSchema(
        id=1,
        customer_name=reservation_data.customer_name,
        table_id=reservation_data.table_id,
        reservation_time=reservation_data.reservation_time,
        duration_minutes=reservation_data.duration_minutes,
    )

    reservation = await service.create_reservation(reservation_data)

    assert reservation.customer_name == "Алиса"
    assert reservation.table_id == 1


@pytest.mark.asyncio
async def test_create_reservation_conflict():
    """Тест на конфликт бронирования (пересечение времени)."""

    mock_repo = AsyncMock(spec=SQLAlchemyAsyncReservationRepository)

    mock_repo.create.side_effect = ReservationConflictException(
        ReservationConflictException.message
    )

    service = ReservationAsyncService(mock_repo)

    reservation_data = ReservationCreateSchema(
        customer_name="Боб",
        table_id=1,
        reservation_time=datetime.now(UTC) + timedelta(days=1),
        duration_minutes=60,
    )

    with pytest.raises(
        ReservationConflictException, match=ReservationConflictException.message
    ):
        await service.create_reservation(reservation_data)
