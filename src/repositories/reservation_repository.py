from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Reservation, Table
from src.exceptions import (
    ReservationNotFoundException,
    ReservationConflictException,
    TableNotFoundException,
)
from sqlalchemy import select
from datetime import timedelta
from src.schemas import (
    ReservationCreateSchema,
    ReservationUpdateSchema,
)


class ReservationAsyncRepositoryInterface(ABC):
    @abstractmethod
    async def create(self, reservation: ReservationCreateSchema) -> Reservation:
        """Добавить новую бронь. Возвращает объект Reservation."""
        pass

    @abstractmethod
    async def get_by_id(self, reservation_id: int) -> Reservation:
        """Найти бронь по ID. Выбрасывает исключение ReservationNotFoundException если не найдена."""
        pass

    @abstractmethod
    async def get_all(self) -> list[Reservation]:
        """Получить все брони."""
        pass

    @abstractmethod
    async def update(self, update_reservation: ReservationUpdateSchema) -> Reservation:
        """Обновить бронь. Возвращает обновленный объект Reservation."""
        pass

    @abstractmethod
    async def delete(self, reservation_id: int) -> None:
        """Удалить бронь по ID."""
        pass


class SQLAlchemyAsyncReservationRepository(ReservationAsyncRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _check_reservations_for_table_by_time(
        self, reservation: ReservationCreateSchema
    ) -> None:
        new_start = reservation.reservation_time
        new_end = new_start + timedelta(minutes=reservation.duration_minutes)
        result = await self.session.execute(
            select(Reservation).filter(
                Reservation.table_id == reservation.table_id,
                Reservation.reservation_time < new_end,
                Reservation.reservation_time
                + timedelta(minutes=reservation.duration_minutes)
                > new_start,
            )
        )
        reservations = result.scalars().first()
        if reservations:
            raise ReservationConflictException()

    async def _check_exists_table_by_id(self, table_id: int) -> None:
        result = await self.session.execute(select(Table).filter(Table.id == table_id))
        table = result.scalars().first()
        if not table:
            raise TableNotFoundException()

    async def create(self, reservation: ReservationCreateSchema) -> Reservation:
        await self._check_exists_table_by_id(reservation.table_id)
        await self._check_reservations_for_table_by_time(reservation)
        new_reservation = Reservation(
            customer_name=reservation.customer_name,
            reservation_time=reservation.reservation_time,
            duration_minutes=reservation.duration_minutes,
            table_id=reservation.table_id,
        )
        self.session.add(new_reservation)
        await self.session.commit()
        return new_reservation

    async def get_by_id(self, reservation_id: int) -> Reservation:
        result = await self.session.execute(
            select(Reservation).filter(Reservation.id == reservation_id)
        )
        reservation = result.scalars().first()
        if not reservation:
            raise ReservationNotFoundException()
        return reservation

    async def get_all(self) -> list[Reservation]:
        result = await self.session.execute(select(Reservation))
        reservations = list(result.scalars().all())
        return reservations

    async def delete(self, reservation_id: int) -> None:
        reservation = await self.get_by_id(reservation_id)
        await self.session.delete(reservation)
        await self.session.commit()

    async def update(self, update_reservation: ReservationUpdateSchema) -> Reservation:
        reservation = await self.get_by_id(update_reservation.reservation_id)

        temp_reservation = ReservationCreateSchema(
            customer_name=update_reservation.customer_name or reservation.customer_name,
            table_id=update_reservation.table_id or reservation.table_id,
            reservation_time=update_reservation.reservation_time
            or reservation.reservation_time,
            duration_minutes=update_reservation.duration_minutes
            or reservation.duration_minutes,
        )

        await self._check_reservations_for_table_by_time(temp_reservation)

        if update_reservation.customer_name:
            reservation.customer_name = update_reservation.customer_name
        if update_reservation.table_id:
            reservation.table_id = update_reservation.table_id
        if update_reservation.reservation_time:
            reservation.reservation_time = update_reservation.reservation_time
        if update_reservation.duration_minutes:
            reservation.duration_minutes = update_reservation.duration_minutes

        await self.session.commit()
        return reservation
