from . import DomainException, NotFoundException, DeletedException


class TableNotFoundException(NotFoundException):
    message = "Столик не найден"


class TableSeatsLimitException(DomainException):
    code = "seats_limit_exceeded"
    status_code = 409
    message = "Недостаточно мест за столиком"


class TableHasReservationsException(DomainException):
    code = "table_has_reservations"
    status_code = 409
    message = "Столик забронирован"


class TableDeletedException(DeletedException):
    message = "Не удалось удалить столик"
