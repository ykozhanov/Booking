class DomainException(Exception):
    code: str = "domain_error"
    status_code = 400
    message: str = "Нарушение бизнес-правила"

    def __init__(self, message: str | None = None, **kwargs):
        self.message = message or self.message
        self.details = kwargs


class NotFoundException(DomainException):
    code = "not_found"
    status_code = 404
    message = "Ресурс не найден"


class DeletedException(DomainException):
    code = "delete_error"
    message = "Не удалось удалить объект"


class ValidationException(DomainException):
    code = "validation_failed"
    message = "Некорректные данные"
