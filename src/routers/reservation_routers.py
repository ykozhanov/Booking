from typing import List

from fastapi import APIRouter, Depends
from src.schemas import (
    ReservationCreateSchema,
    ReservationResponseSchema,
    ResponseSchema,
    ValidationErrorResponseSchema,
)
from src.services import ReservationAsyncService
from src.dependencies import get_reservation_async_service

router = APIRouter()


@router.get(
    "/",
    response_model=List[ReservationResponseSchema],
    summary="Получить все брони",
    responses={
        200: {"description": "Успешный ответ"},
        500: {"description": "Внутренняя ошибка сервера", "model": ResponseSchema},
    },
)
async def get_reservations(
    service: ReservationAsyncService = Depends(get_reservation_async_service),
) -> list[ReservationResponseSchema]:
    """Получить все брони"""
    return await service.get_all_reservations()


@router.post(
    "/",
    response_model=ReservationResponseSchema,
    status_code=201,
    summary="Создать новую бронь",
    responses={
        201: {"description": "Успешное создание"},
        404: {"description": "Столик для брони не найден", "model": ResponseSchema},
        422: {
            "description": "Некорректные данные",
            "model": ValidationErrorResponseSchema,
        },
        500: {"description": "Внутренняя ошибка сервера", "model": ResponseSchema},
    },
)
async def create_reservation(
    reservation: ReservationCreateSchema,
    service: ReservationAsyncService = Depends(get_reservation_async_service),
) -> ReservationResponseSchema:
    """
    Создать новую бронь. Время должно быть в ISO формате с таймзоной (например: 2025-01-01T00:00:01Z), без миллисекунд
    """
    return await service.create_reservation(reservation)


@router.delete(
    "/{reservation_id}",
    status_code=204,
    summary="Удалить бронь по ID",
    responses={
        204: {"description": "Успешное удаление"},
        404: {"description": "Бронь не найдена"},
        422: {
            "description": "Некорректные данные",
            "model": ValidationErrorResponseSchema,
        },
        500: {"description": "Внутренняя ошибка сервера", "model": ResponseSchema},
    },
)
async def delete_reservation(
    reservation_id: int,
    service: ReservationAsyncService = Depends(get_reservation_async_service),
) -> None:
    """Удалить бронь по ID"""
    await service.delete_reservation(reservation_id)
