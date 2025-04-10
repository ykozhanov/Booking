from fastapi import APIRouter, HTTPException, Depends
from src.schemas import TableCreateSchema, TableResponseSchema
from src.services.table_service import TableService
from src.dependencies import get_table_service
from src.exceptions import DomainException, NotFoundException

router = APIRouter()


@router.get("/", response_model=list(TableResponseSchema))
async def get_tables(service: TableService = Depends(get_table_service)):
    try:
        return await service.get_all_tables()
    except DomainException as e:
        raise HTTPException(status_code=400, detail=e.details)


@router.post("/", response_model=TableResponseSchema, status_code=201)
async def create_table(
    table: TableCreateSchema, service: TableService = Depends(get_table_service)
) -> TableResponseSchema:
    try:
        return await service.create_table(table)
    except DomainException as e:
        raise HTTPException(status_code=400, detail=e.details)


@router.delete("/{table_id}", response_model=dict[str, str])
async def delete_table(
    table_id: int, service: TableService = Depends(get_table_service)
):
    try:
        await service.delete_table(table_id)
        return {"message": "Таблица успешно удалена"}
    except DomainException as e:
        if e.code == NotFoundException.code:
            status_code = 404
        else:
            status_code = 400
        raise HTTPException(status_code=status_code, detail=e.details)
