from dataclasses import dataclass
from typing import Literal

from pydantic import BaseModel, Field
from rest_framework.views import APIView

from common.interface.response import error_response, success_response
from common.interface.validators import validate_body, validate_query_params
from common.service.token.exception import PagingException
from macro_sheet.domain.block.block import Block
from macro_sheet.service.exception.exceptions import (
    FunctionException,
    FunctionHasChildrenException,
)
from macro_sheet.usecase.block_function_usecase import BlockFunctionUseCase
from user.domain.user_role import UserRoles
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

    @validate_token(roles=UserRoles.USER_ROLES)
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


class MYBlockFunctionView(APIView):
    """
    user 토큰을 까서 해당 유저의 function 관련 view
    """

    class CreateBodyParams(BaseModel):
        name: str = Field(default="unknown", max_length=255)
        blocks: list
        raw_blocks: list

    class UpdateBodyParams(BaseModel):
        name: str = Field(default="unknown", max_length=255)
        blocks: list
        raw_blocks: list

    class DeleteQueryParams(BaseModel):
        mode: Literal["safe", "simple"] = "safe"

    def __init__(self):
        self.block_function_use_case = BlockFunctionUseCase()

    @validate_token(roles=UserRoles.USER_ROLES)
    def get(self, request, function_id: str, token_payload: UserTokenPayload):
        """
        넘겨준 function_id 에 해당되는 내용을 반환
        """
        try:
            function = self.block_function_use_case.fetch_process(
                function_id=function_id
            )

        except FunctionException as e:
            return error_response(
                code=e.code, message=str(e), status=400, detail=e.detail
            )

        if function.owner_id != token_payload.user_id:
            return error_response(message="권한이 없습니다.")

        dicted_function = function.to_dict()
        return success_response(
            data=dicted_function, message="성공적인 fetch올시다", status=200
        )

    @validate_token(roles=UserRoles.USER_ROLES)
    @validate_body(CreateBodyParams)
    def post(self, request, token_payload: UserTokenPayload, body: CreateBodyParams):
        """
        block function 생성.
        """
        try:
            blocks_vo = [Block.from_dict(block) for block in body.blocks]
            function = self.block_function_use_case.create_process(
                owner_id=token_payload.user_id,  # type: ignore
                name=body.name,
                blocks=blocks_vo,
                raw_blocks=body.raw_blocks,
            )

            return success_response(
                data="", message=f"function id {function.id}가 생성되었소", status=201
            )

        except FunctionException as e:
            return error_response(
                code=e.code, message=str(e), status=400, detail=e.detail
            )

        except (ValueError, AttributeError) as e:
            return error_response(message="유효하지 않은 블록 형식입니다.", status=400)

    @validate_token(roles=UserRoles.USER_ROLES)
    @validate_body(UpdateBodyParams)
    def put(
        self,
        request,
        function_id: str,
        token_payload: UserTokenPayload,
        body: UpdateBodyParams,
    ):
        """
        worksheet id 에 해당되는 worksheet 를 수정한다.
        """
        try:
            block_function = self.block_function_use_case.fetch_process(
                function_id=function_id
            )

            if block_function.owner_id != token_payload.user_id:
                return error_response(message="권한이 없습니다.")

            blocks_vo = [Block.from_dict(block) for block in body.blocks]

            self.block_function_use_case.update_process(
                function_id=function_id,
                owner_id=token_payload.user_id,
                name=body.name,
                raw_blocks=body.raw_blocks,
                blocks=blocks_vo,
            )

            return success_response(
                data="", message=f"block function id {function_id}가 변경되었소", status=200
            )

        except FunctionException as e:
            return error_response(
                code=e.code, message=str(e), status=400, detail=e.detail
            )

        except (ValueError, AttributeError) as e:
            return error_response(message="유효하지 않은 블록 형식입니다.", status=400)

    @validate_token(roles=UserRoles.USER_ROLES)
    @validate_query_params(DeleteQueryParams)
    def delete(
        self,
        request,
        function_id: str,
        token_payload: UserTokenPayload,
        params: DeleteQueryParams,
    ):
        """
        worksheet id 에 해당되는 worksheet 를 삭제한다.
        """
        try:
            worksheet = self.block_function_use_case.fetch_process(
                function_id=function_id
            )
            if worksheet.owner_id != token_payload.user_id:
                return error_response(message="권한이 없습니다.")
            if params.mode == "simple":
                self.block_function_use_case.delete_process(function_id=function_id)

            if params.mode == "safe":
                self.block_function_use_case.safety_delete_process(
                    function_id=function_id
                )

            return success_response(
                data="", message=f"block function id {function_id}가 삭제되었소", status=200
            )

        except FunctionHasChildrenException as e:
            return error_response(
                code=e.code, message=str(e), status=409, detail=e.detail
            )

        except FunctionException as e:
            return error_response(
                code=e.code, message=str(e), status=400, detail=e.detail
            )


class FunctionValidatorView(APIView):
    def __init__(self) -> None:
        self.function_use_case = BlockFunctionUseCase()

    @dataclass
    class BodyParams(BaseModel):
        blocks: list
        raw_blocks: list
        name: str = Field(default="unknown", max_length=255)

    @validate_token(roles=UserRoles.ALL_USER_ROLES)
    @validate_body(BodyParams)
    def post(self, request, token_payload: UserTokenPayload, body: BodyParams):
        # TODO: 뭔가 나중에 user, guest 에 따라서 validate를 다르게 할수있을듯.
        blocks_vo = [Block.from_dict(block) for block in body.blocks]
        result = self.function_use_case.validate_function(blocks=blocks_vo)
        if result:
            data = {"target": result, "is_valid": False}
            return success_response(
                message=f"존재하지않는 function을 참조하고있습니다", status=200, data=data
            )

        return success_response(
            data={"target": result, "is_valid": True}, message=f"valid", status=200
        )
