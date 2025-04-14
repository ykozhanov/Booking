from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Reservation
from src.exceptions import ReservationNotFoundException
from sqlalchemy import select, func, DateTime, Interval
from datetime import timedelta, datetime
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
        """Получить бронь по ID. Выбрасывает исключение ReservationNotFoundException если не найдена."""
        pass

    @abstractmethod
    async def get_by_table_id(self, table_id: int) -> list[Reservation]:
        """Получить все брони для столика"""
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

    @abstractmethod
    async def get_reservations_for_table_by_time(
        self, table_id: int, reservation_time: datetime, duration_minutes: int
    ) -> list[Reservation]:
        """Получить все брони для столика в указанный период"""
        pass


class SQLAlchemyAsyncReservationRepository(ReservationAsyncRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_reservations_for_table_by_time(
        self, table_id: int, reservation_time: datetime, duration_minutes: int
    ) -> list[Reservation]:
        end_time = reservation_time + timedelta(minutes=duration_minutes)

        result = await self.session.execute(
            select(Reservation).filter(
                Reservation.table_id == table_id,
                Reservation.reservation_time
                < func.cast(end_time, DateTime(timezone=True)),
                func.cast(Reservation.reservation_time, DateTime(timezone=True))
                + func.cast(timedelta(minutes=duration_minutes), Interval)
                > func.cast(reservation_time, DateTime(timezone=True)),
            )
        )
        return list(result.scalars().all())

    async def get_by_table_id(self, table_id: int) -> list[Reservation]:
        reservations = await self.session.execute(
            select(Reservation).filter(Reservation.table_id == table_id)
        )
        return list(reservations.scalars().all())

    async def create(self, reservation: ReservationCreateSchema) -> Reservation:
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
