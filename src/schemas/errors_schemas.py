from pydantic import BaseModel


class ErrorResponseSchema(BaseModel):
    message: str


class ValidationErrorResponseSchema(ErrorResponseSchema):
    detail: dict[str, str]
