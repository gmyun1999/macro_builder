from dataclasses import dataclass
from typing import Any

from django.http import JsonResponse
from pydantic import BaseModel, Field
from rest_framework import status
from rest_framework.views import APIView

from common.domain import PagedResult
from common.interface.response import error_response, success_response
from common.interface.validators import validate_body, validate_query_params
from common.response_msg import TokenMessage
from common.service.token.exception import PagingException
from macro_sheet.domain.block.base_block.main_block import MainBlock
from macro_sheet.domain.block.block import Block
from macro_sheet.service.exception.exceptions import (
    FunctionException,
    WorksheetException,
)
from macro_sheet.service.i_repo.i_worksheet_repo import IWorksheetRepo
from macro_sheet.usecase.block_function_usecase import BlockFunctionUseCase
from macro_sheet.usecase.worksheet_usecase import WorksheetUseCase
from user.domain.user_token import UserTokenPayload
from user.interface.validator.user_token_validator import validate_token


class GETMyFunctionListView(APIView):
    """
    user 토큰을 까서 해당 user 의 functions들을 반환한다.
    """

    @dataclass
    class QueryParams(BaseModel):
        page: int = Field(default=1, gt=0)
        page_size: int = Field(default=10, gt=0)

    def __init__(self):
        self.function_use_case = BlockFunctionUseCase()

    @validate_token()
    @validate_query_params(QueryParams)
    def get(self, request, token_payload: UserTokenPayload, params: QueryParams):
        user_id: str = token_payload.user_id  # type: ignore
        page = params.page
        page_size = params.page_size
        try:
            paged_result = self.function_use_case.bulk_fetch_process(
                owner_id=user_id, page=page, page_size=page_size
            )

            response_data = {
                "items": [item.to_dict() for item in paged_result.items],
                "total_items": paged_result.total_items,
                "total_pages": paged_result.total_pages,
                "current_page": paged_result.current_page,
                "page_size": paged_result.page_size,
                "has_previous": paged_result.has_previous,
                "has_next": paged_result.has_next,
            }

            return success_response(data=response_data, message="함수 조회에 성공했습니다.")

        except PagingException as e:
            return error_response(code=e.code, message=str(e), status=400)
