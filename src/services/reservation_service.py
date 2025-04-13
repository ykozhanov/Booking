from datetime import datetime

from src.repositories import (
    ReservationAsyncRepositoryInterface,
    TableAsyncRepositoryInterface,
)
from src.schemas import (
    ReservationUpdateSchema,
    ReservationCreateSchema,
    ReservationResponseSchema,
)
from src.exceptions import ReservationConflictException


class ReservationAsyncService:
    def __init__(
        self,
        reservation_repository: ReservationAsyncRepositoryInterface,
        table_repository: TableAsyncRepositoryInterface,
    ):
        self.reservation_repository = reservation_repository
        self.table_repository = table_repository

    async def get_all_reservations(self) -> list[ReservationResponseSchema]:
        """Получить все брони."""
        reservations = await self.reservation_repository.get_all()
        return [ReservationResponseSchema.model_validate(r) for r in reservations]

    async def _check_exists_table(self, table_id: int) -> None:
        await self.table_repository.get_by_id(table_id)

    async def _check_conflict_reservations(
        self, table_id: int, reservation_time: datetime, duration_minutes: int
    ) -> None:
        reservations = (
            await self.reservation_repository.get_reservations_for_table_by_time(
                table_id, reservation_time, duration_minutes
            )
        )
        if reservations:
            raise ReservationConflictException()

    async def create_reservation(
        self, reservation: ReservationCreateSchema
    ) -> ReservationResponseSchema:
        """Создать новую бронь."""
        await self._check_conflict_reservations(
            reservation.table_id,
            reservation.reservation_time,
            reservation.duration_minutes,
        )
        await self._check_exists_table(reservation.table_id)
        new_reservation = await self.reservation_repository.create(reservation)
        return ReservationResponseSchema.model_validate(new_reservation)

    async def delete_reservation(self, reservation_id: int) -> None:
        """Удалить бронь по ID."""
        await self.reservation_repository.delete(reservation_id)

    async def _check_update_reservation_time(
        self, update_reservation: ReservationUpdateSchema
    ) -> None:
        if (
            update_reservation.reservation_time is None
            or update_reservation.duration_minutes is None
        ):
            old_reservation = await self.reservation_repository.get_by_id(
                update_reservation.id
            )
            if update_reservation.reservation_time is None:
                update_reservation.reservation_time = old_reservation.reservation_time
            if update_reservation.duration_minutes is None:
                update_reservation.duration_minutes = old_reservation.duration_minutes

        if update_reservation.duration_minutes:
            await self._check_conflict_reservations(
                update_reservation.table_id,
                update_reservation.reservation_time,
                update_reservation.duration_minutes,
            )

    async def update_reservation(
        self, update_reservation: ReservationUpdateSchema
    ) -> ReservationResponseSchema:
        """Обновить бронь."""
        await self._check_update_reservation_time(update_reservation)
        updated_reservation = await self.reservation_repository.update(
            update_reservation
        )
        return ReservationResponseSchema.model_validate(updated_reservation)
