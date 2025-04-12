from typing import Dict, List

from fastapi import APIRouter, HTTPException, Depends
from src.schemas import TableCreateSchema, TableResponseSchema
from src.services import TableAsyncService
from src.dependencies import get_table_async_service
from src.exceptions import DomainException, NotFoundException

router = APIRouter()


@router.get(
    "/", response_model=List[TableResponseSchema], summary="Получить все столики"
)
async def get_tables(service: TableAsyncService = Depends(get_table_async_service)):
    """Получить все столики"""
    try:
        return await service.get_all_tables()
    except DomainException as e:
        raise HTTPException(status_code=400, detail=e.details)
    except Exception as e:
        #TODO Настроить логирование ошибок + тех, что выше
        raise HTTPException(status_code=400, detail="Что-то пошло не так")


@router.post(
    "/",
    response_model=TableResponseSchema,
    status_code=201,
    summary="Создать новый столик",
)
async def create_table(
    table: TableCreateSchema,
    service: TableAsyncService = Depends(get_table_async_service),
) -> TableResponseSchema:
    """Создать новый столик"""
    try:
        return await service.create_table(table)
    except DomainException as e:
        raise HTTPException(status_code=400, detail=e.details)
    except Exception as e:
        #TODO Настроить логирование ошибок + тех, что выше
        raise HTTPException(status_code=400, detail="Что-то пошло не так")


@router.delete(
    "/{table_id}",
    response_model=Dict[str, str],
    summary="Удалить столик по ID",
    responses={
        404: {"description": "Столик не найден"},
    },
)
async def delete_table(
    table_id: int, service: TableAsyncService = Depends(get_table_async_service)
):
    """Удалить столик по ID"""
    try:
        await service.delete_table(table_id)
        return {"message": "Таблица успешно удалена"}
    except DomainException as e:
        if e.code == NotFoundException.code:
            status_code = 404
        else:
            status_code = 400
        raise HTTPException(status_code=status_code, detail=e.details)
    except Exception as e:
        #TODO Настроить логирование ошибок + тех, что выше
        raise HTTPException(status_code=400, detail="Что-то пошло не так")
