from typing import List

from fastapi import APIRouter, Depends
from src.schemas import (
    TableCreateSchema,
    TableResponseSchema,
    ResponseSchema,
    ValidationErrorResponseSchema,
)
from src.services import TableAsyncService
from src.dependencies import get_table_async_service

router = APIRouter()


@router.get(
    "/",
    response_model=List[TableResponseSchema],
    summary="Получить все столики",
    responses={
        200: {"description": "Успешный ответ"},
        500: {"description": "Внутренняя ошибка сервера", "model": ResponseSchema},
    },
)
async def get_tables(
    service: TableAsyncService = Depends(get_table_async_service),
) -> list[TableResponseSchema]:
    """Получить все столики"""
    return await service.get_all_tables()


@router.post(
    "/",
    response_model=TableResponseSchema,
    status_code=201,
    summary="Создать новый столик",
    responses={
        201: {"description": "Успешное создание"},
        422: {
            "description": "Некорректные данные",
            "model": ValidationErrorResponseSchema,
        },
        500: {"description": "Внутренняя ошибка сервера", "model": ResponseSchema},
    },
)
async def create_table(
    table: TableCreateSchema,
    service: TableAsyncService = Depends(get_table_async_service),
) -> TableResponseSchema:
    """Создать новый столик"""
    return await service.create_table(table)


@router.delete(
    "/{table_id}",
    status_code=204,
    summary="Удалить столик по ID",
    responses={
        204: {"description": "Успешное удаление"},
        404: {"description": "Столик не найден", "model": ResponseSchema},
        422: {
            "description": "Некорректные данные",
            "model": ValidationErrorResponseSchema,
        },
        500: {"description": "Внутренняя ошибка сервера", "model": ResponseSchema},
    },
)
async def delete_table(
    table_id: int, service: TableAsyncService = Depends(get_table_async_service)
) -> None:
    """Удалить столик по ID"""
    await service.delete_table(table_id)
