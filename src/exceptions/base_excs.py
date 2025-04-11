class DomainException(Exception):
    code: str = "domain_error"
    message: str = "Нарушение бизнес-правила"

    def __init__(self, message: str | None = None, **kwargs):
        self.message = message or self.message
        self.details = kwargs


class NotFoundException(DomainException):
    code = "not_found"
    message = "Ресурс не найден"


class DeletedException(DomainException):
    code = "delete_error"
    message = "Не удалось удалить объект"


class ValidationException(DomainException):
    code = "validation_failed"
    message = "Некорректные данные"
