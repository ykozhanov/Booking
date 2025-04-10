from typing import Any

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator
from src.exceptions import ValidationException


class TableCreateSchema(BaseModel):
    customer_name: str
    name: str
    seats: int = Field(..., gt=0)
    location: str


class TableUpdateSchema(BaseModel):
    id: int
    name: str | None = None
    seats: int | None = None
    location: str | None = None

    @field_validator("seats")
    @classmethod
    def validate_seats(cls, v: Any):
        if v is not None and v <= 0:
            raise ValidationException("Мест за столом должно быть больше 0.")
        return v


class TableResponseSchema(TableCreateSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)
