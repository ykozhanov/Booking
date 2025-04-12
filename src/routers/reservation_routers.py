from typing import Dict, List

from fastapi import APIRouter, HTTPException, Depends
from src.schemas import (
    ReservationCreateSchema,
    ReservationResponseSchema,
)
from src.services import ReservationAsyncService
from src.dependencies import get_reservation_async_service
from src.exceptions import DomainException, NotFoundException

router = APIRouter()


@router.get(
    "/", response_model=List[ReservationResponseSchema], summary="Получить все брони"
)
async def get_tables(
    service: ReservationAsyncService = Depends(get_reservation_async_service),
):
    """Получить все брони"""
    try:
        return await service.get_all_reservations()
    except DomainException as e:
        raise HTTPException(status_code=400, detail=e.details)
    except Exception as e:
        #TODO Настроить логирование ошибок + тех, что выше
        raise HTTPException(status_code=400, detail="Что-то пошло не так")


@router.post(
    "/",
    response_model=ReservationResponseSchema,
    status_code=201,
    summary="Создать новую бронь",
)
async def create_reservation(
    reservation: ReservationCreateSchema,
    service: ReservationAsyncService = Depends(get_reservation_async_service),
):
    """Создать новую бронь"""
    try:
        return await service.create_reservation(reservation)
    except DomainException as e:
        raise HTTPException(status_code=400, detail=e.details)
    except Exception as e:
        #TODO Настроить логирование ошибок + тех, что выше
        raise HTTPException(status_code=400, detail=f"Что-то пошло не так: {str(e)}")


@router.delete(
    "/{reservation_id}",
    response_model=Dict[str, str],
    summary="Удалить бронь по ID",
    responses={
        404: {"description": "Бронь не найдена"},
    },
)
async def delete_reservation(
    reservation_id: int,
    service: ReservationAsyncService = Depends(get_reservation_async_service),
):
    """Удалить бронь по ID"""
    try:
        await service.delete_reservation(reservation_id)
        return {"message": "Бронь успешно удалена"}
    except DomainException as e:
        if e.code == NotFoundException.code:
            status_code = 404
        else:
            status_code = 400
        raise HTTPException(status_code=status_code, detail=e.details)
    except Exception as e:
        #TODO Настроить логирование ошибок + тех, что выше
        raise HTTPException(status_code=400, detail="Что-то пошло не так")
