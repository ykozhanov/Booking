from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from src.routers import table_router, reservation_router

app = FastAPI()

@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=400,
        content={"detail": exc.errors()},
    )

app.include_router(table_router, prefix="/tables", tags=["tables"])
app.include_router(reservation_router, prefix="/reservations", tags=["reservations"])
