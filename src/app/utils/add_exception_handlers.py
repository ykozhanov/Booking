from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from src.exceptions import DomainException


def add_exception_handlers(app: FastAPI) -> None:
    # Кастомные исключения
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.detail},
            headers=exc.headers,
        )

    # Ошибки валидации Pydantic
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        return JSONResponse(
            status_code=422,
            content={"error": "Некорректные данные", "details": exc.errors()},
        )

    # Все остальные исключения
    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        # Логируем ошибку (например, в Sentry)
        logger.error(f"Unexpected error: {str(exc)}", exc_info=True)

        return JSONResponse(
            status_code=500, content={"error": "Внутренняя ошибка сервера"}
        )
