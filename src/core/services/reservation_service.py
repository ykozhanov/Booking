from datetime import timedelta

from src.core.domain import Reservation
from src.application.interfaces import ReservationRepository, TableRepository
from src.core.exceptions import ReservationConflictException


class ReservationService:
    def __init__(self, repo: ReservationRepository, table_repo: TableRepository):
        self.repo = repo
        self.table_repo = table_repo

    def get_reservation_by_id(self, reservation_id: int) -> Reservation:
        return self.repo.get_by_id(reservation_id)

    def _check_exists_table(self, table_id: int) -> None:
        self.table_repo.get_by_id(table_id)

    def _check_conflicting(self, reservation: Reservation) -> None:
        conflicting = self.repo.get_for_table_by_time(
            reservation.table_id,
            start_time=reservation.reservation_time,
            end_time=reservation.reservation_time
            + timedelta(minutes=reservation.duration_minutes),
        )
        if conflicting:
            raise ReservationConflictException("Столик занят")

    def create(self, reservation: Reservation) -> Reservation:
        self._check_exists_table(reservation.table_id)
        self._check_conflicting(reservation)
        return self.repo.add(reservation)

    def delete(self, reservation_id: int) -> None:
        reservation = self.repo.get_by_id(reservation_id)
        self.repo.delete(reservation.id)
