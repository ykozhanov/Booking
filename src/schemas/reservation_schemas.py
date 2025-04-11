from typing import Any

from pydantic import BaseModel, ConfigDict, field_validator, Field
from datetime import datetime, UTC
from src.exceptions import ValidationException


class ReservationCreateSchema(BaseModel):
    customer_name: str
    table_id: int
    reservation_time: datetime
    duration_minutes: int = Field(..., gt=0)

    @field_validator("reservation_time")
    @classmethod
    def validate_reservation_time(cls, v: Any):
        if v and v < datetime.now(UTC):
            raise ValidationException("Время бронирования не может быть в прошлом.")
        return v


class ReservationUpdateSchema(BaseModel):
    id: int
    customer_name: str | None = None
    table_id: int | None = None
    reservation_time: datetime | None = None
    duration_minutes: int | None = None

    @field_validator("reservation_time")
    @classmethod
    def validate_reservation_time(cls, v: Any):
        if v and v < datetime.now(UTC):
            raise ValidationException("Время бронирования не может быть в прошлом.")
        return v

    @field_validator("duration_minutes")
    @classmethod
    def validate_seats(cls, v: Any):
        if v is not None and v <= 0:
            raise ValidationException("Длительность брони должна быть больше 0.")
        return v


class ReservationResponseSchema(ReservationCreateSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)
