from fastapi import Depends

from src.services import TableAsyncService, ReservationAsyncService
from src.repositories import SQLAlchemyAsyncTableRepository, SQLAlchemyAsyncReservationRepository
from src.db import get_session
from sqlalchemy.ext.asyncio import AsyncSession


# Зависимость для сервиса столиков
def get_table_async_service(db: AsyncSession = Depends(get_session)) -> TableAsyncService:
    return TableAsyncService(SQLAlchemyAsyncTableRepository(db))


# Зависимость для сервиса бронирований
def get_reservation_async_service(
    db: AsyncSession = Depends(get_session),
) -> ReservationAsyncService:
    return ReservationAsyncService(SQLAlchemyAsyncReservationRepository(db))
