from fastapi import APIRouter, HTTPException, Depends
from src.schemas import (
    ReservationCreateSchema,
    ReservationResponseSchema,
)
from src.services.reservation_service import ReservationService
from src.dependencies import get_reservation_service
from src.exceptions import DomainException, NotFoundException

router = APIRouter()


@router.get("/", response_model=list(ReservationResponseSchema))
async def get_tables(service: ReservationService = Depends(get_reservation_service)):
    try:
        return await service.get_all_reservations()
    except DomainException as e:
        raise HTTPException(status_code=400, detail=e.details)


@router.post(
    "/", response_model=ReservationResponseSchema, status_code=201
)
async def create_reservation(
    reservation: ReservationCreateSchema,
    service: ReservationService = Depends(get_reservation_service),
):
    try:
        return await service.create_reservation(reservation)
    except DomainException as e:
        raise HTTPException(status_code=400, detail=e.details)


@router.delete("/{reservation_id}", response_model=dict[str, str])
async def delete_reservation(
    reservation_id: int, service: ReservationService = Depends(get_reservation_service)
):
    try:
        await service.delete_reservation(reservation_id)
        return {"message": "Бронь успешно удалена"}
    except DomainException as e:
        if e.code == NotFoundException.code:
            status_code = 404
        else:
            status_code = 400
        raise HTTPException(status_code=status_code, detail=e.details)
