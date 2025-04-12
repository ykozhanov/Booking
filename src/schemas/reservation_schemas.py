from pydantic import BaseModel, ConfigDict, field_validator, Field
from datetime import datetime, timezone


class ReservationCreateSchema(BaseModel):
    customer_name: str
    table_id: int
    reservation_time: datetime
    duration_minutes: int = Field(..., gt=0)

    @field_validator("reservation_time")
    @classmethod
    def validate_reservation_time(cls, v: datetime):
        if v.tzinfo is None:
            raise ValueError(
                "Время должно быть в ISO формате с таймзоной (например: 2025-01-01T00:00:01Z), без миллисекунд"
            )

        v_utc = v.astimezone(timezone.utc)
        if v_utc < datetime.now(timezone.utc):
            raise ValueError("Время бронирования не может быть в прошлом.")

        return v.replace(tzinfo=None)


class ReservationUpdateSchema(BaseModel):
    id: int
    customer_name: str | None = None
    table_id: int | None = None
    reservation_time: datetime | None = None
    duration_minutes: int | None = Field(None, gt=0)

    @field_validator("reservation_time")
    @classmethod
    def validate_reservation_time(cls, v: datetime | None):
        if v:
            if v.tzinfo is None:
                raise ValueError(
                    "Время должно быть в ISO формате с таймзоной (например: 2025-01-01T00:00:01Z), без миллисекунд"
                )

            v_utc = v.astimezone(timezone.utc)
            if v_utc < datetime.now(timezone.utc):
                raise ValueError("Время бронирования не может быть в прошлом.")

            return v.replace(tzinfo=None)


class ReservationResponseSchema(ReservationCreateSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)
