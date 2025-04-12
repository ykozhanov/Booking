from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from src.schemas import (
    ResponseSchema,
    ValidationErrorResponseSchema,
    ValidationErrorDetail,
)
from src.exceptions import DomainException
from src.core.config import logger


def add_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(DomainException)
    async def domain_exception_handler(request: Request, exc: DomainException):
        """Кастомные исключения"""
        logger.exception(
            f"Исключение: {exc.code}\n"
            f"Статус код: {exc.status_code}\n"
            f"Сообщение: {exc.message}\n"
            f"Детали: {exc.details}\n",
            exc_info=True,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=dict(ResponseSchema(message=exc.message)),
        )

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        """Ошибки валидации Pydantic при запросе"""
        list_detail = [ValidationErrorDetail(**d) for d in exc.errors()]
        logger.exception(
            f"Исключение: RequestValidationError:\n"
            f"Статус код: 422\n"
            f"Детали: {list_detail}\n",
            exc_info=True,
        )
        return JSONResponse(
            status_code=422,
            content=ValidationErrorResponseSchema(
                message="Некорректные данные",
                detail=list_detail,
            ).model_dump(),
        )

    @app.exception_handler(ValidationError)
    async def validation_exception_handler(request: Request, exc: ValidationError):
        """Ошибки валидации Pydantic при работе с данными"""
        list_detail = [ValidationErrorDetail(**d) for d in exc.errors()]
        logger.exception(
            f"Исключение: ValidationError:\n"
            f"Статус код: 422\n"
            f"Детали: {list_detail}\n"
        )
        return JSONResponse(
            status_code=422,
            content=ValidationErrorResponseSchema(
                message="Некорректные данные",
                detail=list_detail,
            ).model_dump(),
        )

    @app.exception_handler(Exception)
    async def other_exception_handler(request: Request, exc: Exception):
        """Все остальные исключения"""
        logger.error(
            f"Исключение: Exception\n" f"Статус код: 500\n" f"Детали: {str(exc)}\n",
            exc_info=True,
        )
        return JSONResponse(
            status_code=500,
            content=dict(ResponseSchema(message="Внутренняя ошибка сервера")),
        )
