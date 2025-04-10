from . import DomainException, NotFoundException, DeletedException

class TableNotFoundException(NotFoundException):
    code = "table_not_found"
    message = "Столик не найден"

class TableSeatsLimitException(DomainException):
    code = "seats_limit_exceeded"
    message = "Недостаточно мест за столиком"

class TableHasReservationsException(DeletedException):
    message = "Столик забронирован"