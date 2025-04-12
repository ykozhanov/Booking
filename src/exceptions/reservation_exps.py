from . import DomainException, NotFoundException, DeletedException


class ReservationConflictException(DomainException):
    code = "reservation_conflict"
    status_code = 409
    message = "Столик уже забронирован на указанное время"


class InvalidReservationTimeException(DomainException):
    code = "invalid_reservation_time"
    message = "Некорректное время бронирования"


class ReservationNotFoundException(NotFoundException):
    message = "Бронь не найдена"


class ReservationDeletedException(DeletedException):
    message = "Не удалось удалить бронь"
