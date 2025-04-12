from pydantic import BaseModel


class ResponseSchema(BaseModel):
    message: str


class ValidationErrorDetail(BaseModel):
    loc: list
    msg: str
    type: str


class ValidationErrorResponseSchema(ResponseSchema):
    detail: list[ValidationErrorDetail]
