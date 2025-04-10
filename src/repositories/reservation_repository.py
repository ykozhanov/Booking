from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Reservation
from src.exceptions import ReservationNotFoundException
from sqlalchemy import select
from datetime import timedelta
from src.schemas import (
    ReservationCreateSchema,
    ReservationUpdateSchema,
)


class ReservationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, reservation: ReservationCreateSchema) -> Reservation:
        """Добавить новую бронь. Возвращает объект Reservation."""
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
        """Найти бронь по ID. Выбрасывает исключение ReservationNotFoundException если не найдена."""
        result = await self.session.execute(
            select(Reservation).filter(Reservation.id == reservation_id)
        )
        reservation = result.scalars().first()
        if not reservation:
            raise ReservationNotFoundException()
        return reservation

    async def get_all(self) -> list[Reservation]:
        """Получить все брони."""
        result = await self.session.execute(select(Reservation))
        reservations = list(result.scalars().all())
        return reservations

    async def delete(self, reservation_id: int) -> None:
        """Удалить бронь по ID."""
        reservation = await self.get_by_id(reservation_id)
        await self.session.delete(reservation)
        await self.session.commit()

    async def update(self, update_reservation: ReservationUpdateSchema) -> Reservation:
        """Обновить бронь. Возвращает обновленный объект Reservation."""
        reservation = await self.get_by_id(update_reservation.reservation_id)
        if not reservation:
            raise ReservationNotFoundException()

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

    async def get_reservations_for_table_by_time(
        self, reservation: ReservationCreateSchema
    ) -> list[Reservation]:
        """Получить все брони для столика в заданном временном промежутке."""
        result = await self.session.execute(
            select(Reservation).filter(
                Reservation.table_id == reservation.table_id,
                Reservation.reservation_time <= reservation.reservation_time,
                Reservation.reservation_time
                >= reservation.reservation_time
                + timedelta(minutes=reservation.duration_minutes),
            )
        )
        reservations = list(result.scalars().all())
        return reservations
