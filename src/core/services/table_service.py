from src.core.domain import Table
from src.application.interfaces import TableRepository, ReservationRepository
from src.core.exceptions import TableHasReservationsException


class TableService:
    def __init__(self, repo: TableRepository, reservation_repo: ReservationRepository):
        self.repo = repo
        self.reservation_repo = reservation_repo

    def get_table_by_id(self, table_id: int) -> Table:
        return self.repo.get_by_id(table_id)

    def create(self, table: Table) -> Table:
        return self.repo.add(table)

    def _check_reservations(self, table_id: int) -> None:
        all_reservation_for_table = self.reservation_repo.get_all_for_table(table_id)
        if all_reservation_for_table:
            raise TableHasReservationsException("У столика имеется бронь")

    def delete(self, table_id: int) -> None:
        table = self.repo.get_by_id(table_id)
        self._check_reservations(table.id)
        self.repo.delete(table.id)
