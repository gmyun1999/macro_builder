from typing import Any

from django.http import JsonResponse


def success_response(
    data: Any, message: str | None = "성공적으로 처리되었습니다.", status: int = 200
):
    return JsonResponse(
        {"status": "success", "data": data, "message": message}, status=status
    )


def error_response(
    code: str | None = None,
    message: str | None = None,
    status: int = 400,
    detail: list[dict] = [],
):
    return JsonResponse(
        {
            "status": "error",
            "error": {"code": code, "message": message, "detail": detail},
        },
        status=status,
    )
