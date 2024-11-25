from typing import Any

from django.http import JsonResponse
from pydantic import BaseModel, Field


class SuccessResponse(BaseModel):
    data: Any
    message: str = Field(default="성공적으로 처리되었습니다.")


def success_response(
    data: Any, message: str = "성공적으로 처리되었습니다.", status: int = 200
) -> JsonResponse:
    response_model = SuccessResponse(data=data, message=message)

    return JsonResponse(
        response_model.model_dump(),
        status=status,
        content_type="application/json; charset=utf-8",
    )


class ErrorDetail(BaseModel):
    code: str | None = None
    message: str | None = None
    detail: dict = Field(default_factory=dict)


class ErrorResponse(BaseModel):
    error: ErrorDetail


def error_response(
    code: str | None = None,
    message: str | None = None,
    status: int = 400,
    detail: dict = {},
) -> JsonResponse:
    response_model = ErrorResponse(
        error=ErrorDetail(code=code, message=message, detail=detail)
    )

    return JsonResponse(
        response_model.model_dump(),
        status=status,
        content_type="application/json; charset=utf-8",
    )
