from fastapi import Depends

from src.services.table_service import TableService
from src.services.reservation_service import ReservationService
from src.repositories.table_repository import TableRepository
from src.repositories.reservation_repository import ReservationRepository
from src.db import get_session
from sqlalchemy.ext.asyncio import AsyncSession


# Зависимость для сервиса столиков
def get_table_service(db: AsyncSession = Depends(get_session)) -> TableService:
    return TableService(TableRepository(db))


# Зависимость для сервиса бронирований
def get_reservation_service(
    db: AsyncSession = Depends(get_session),
) -> ReservationService:
    return ReservationService(ReservationRepository(db))
