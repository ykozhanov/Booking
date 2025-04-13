from fastapi import Depends

from src.services import TableAsyncService, ReservationAsyncService
from src.repositories import (
    SQLAlchemyAsyncTableRepository,
    SQLAlchemyAsyncReservationRepository,
)
from src.core.db import get_session
from sqlalchemy.ext.asyncio import AsyncSession


# Зависимость для сервиса столиков
def get_table_async_service(
    db: AsyncSession = Depends(get_session),
) -> TableAsyncService:
    table_repository = SQLAlchemyAsyncTableRepository(db)
    reservation_repository = SQLAlchemyAsyncReservationRepository(db)
    return TableAsyncService(table_repository, reservation_repository)


# Зависимость для сервиса бронирований
def get_reservation_async_service(
    db: AsyncSession = Depends(get_session),
) -> ReservationAsyncService:
    table_repository = SQLAlchemyAsyncTableRepository(db)
    reservation_repository = SQLAlchemyAsyncReservationRepository(db)
    return ReservationAsyncService(reservation_repository, table_repository)
