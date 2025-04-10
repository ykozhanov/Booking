from . import DomainException, NotFoundException


class ReservationConflictException(DomainException):
    code = "reservation_conflict"
    message = "Столик уже забронирован на указанное время"


class InvalidReservationTimeException(DomainException):
    code = "invalid_reservation_time"
    message = "Некорректное время бронирования"


class ReservationNotFoundException(NotFoundException):
    code = "reservation_not_found"
    message = "Бронь не найдена"