from src.repositories import ReservationAsyncRepositoryInterface
from src.schemas import (
    ReservationUpdateSchema,
    ReservationCreateSchema,
    ReservationResponseSchema,
)


class ReservationAsyncService:
    def __init__(self, reservation_repository: ReservationAsyncRepositoryInterface):
        self.reservation_repository = reservation_repository

    async def get_all_reservations(self) -> list[ReservationResponseSchema]:
        """Получить все брони."""
        reservations = await self.reservation_repository.get_all()
        return [ReservationResponseSchema.model_validate(r) for r in reservations]

    async def create_reservation(
        self, reservation: ReservationCreateSchema
    ) -> ReservationResponseSchema:
        """Создать новую бронь."""
        new_reservation = await self.reservation_repository.create(reservation)
        return ReservationResponseSchema.model_validate(new_reservation)

    async def delete_reservation(self, reservation_id: int) -> None:
        """Удалить бронь по ID."""
        await self.reservation_repository.delete(reservation_id)

    async def update_reservation(
        self, update_reservation: ReservationUpdateSchema
    ) -> ReservationResponseSchema:
        """Обновить бронь."""
        updated_reservation = await self.reservation_repository.update(
            update_reservation
        )
        return ReservationResponseSchema.model_validate(updated_reservation)
