from fastapi import FastAPI
from src.utils import add_routers, add_exception_handlers

app = FastAPI(
    title="Booking",
    description="Микросервис для бронирования столиков в ресторане с поддержкой временных слотов и проверкой конфликтов",
    version="0.0.1",
)

add_routers(app)
add_exception_handlers(app)
