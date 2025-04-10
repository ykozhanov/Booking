from fastapi import FastAPI
from src.routers import table_router, reservation_router

app = FastAPI()

app.include_router(table_router, prefix="/tables", tags=["tables"])
app.include_router(reservation_router, prefix="/reservations", tags=["reservations"])
