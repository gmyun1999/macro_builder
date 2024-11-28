from dataclasses import dataclass
from typing import Any

from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from pydantic import BaseModel, Field
from rest_framework.views import APIView

from common.domain import PagedResult
from common.interface.response import (
    ErrorResponse,
    SuccessResponse,
    error_response,
    success_response,
)
from common.interface.validators import validate_body, validate_query_params
from common.service.token.exception import PagingException
from macro_sheet.domain.block.base_block.main_block import MainBlock
from macro_sheet.domain.block.block import Block
from macro_sheet.service.exception.exceptions import (
    FunctionException,
    WorksheetException,
)
from macro_sheet.service.i_repo.i_worksheet_repo import IWorksheetRepo
from macro_sheet.usecase.worksheet_usecase import WorksheetUseCase
from user.domain.user_role import UserRoles
from user.domain.user_token import UserTokenPayload
from user.interface.validator.user_token_validator import validate_token
from util.pydantic_serializer import PydanticToDjangoSerializer


class GETMyWorksheetListView(APIView):
    """
    user 토큰을 까서 해당 user 의 worksheets들을 반환한다.
    """

    @dataclass
    class QueryParams(BaseModel):
        page: int = Field(default=1, gt=0)
        page_size: int = Field(default=10, gt=0)

    def __init__(self):
        self.worksheet_use_case = WorksheetUseCase()

    @extend_schema(
        summary="나의 worksheet를 넘겨줘서 가져온다.",
        description=", page, page_size를 query params로 넘겨줘서 페이징처리 가능",
        parameters=[
            OpenApiParameter(
                name="page",
                type=int,
                location=OpenApiParameter.QUERY,
                required=False,
                description="페이지 번호 (기본값: 1)",
                default=1,
            ),
            OpenApiParameter(
                name="page_size",
                type=int,
                location=OpenApiParameter.QUERY,
                required=False,
                description="페이지 크기 (기본값: 10)",
                default=10,
            ),
        ],
        responses={
            201: OpenApiResponse(
                PydanticToDjangoSerializer.convert(SuccessResponse),
                description="성공적인 응답",
            ),
            400: OpenApiResponse(
                PydanticToDjangoSerializer.convert(ErrorResponse),
                description="페이징 에러",
            ),
            403: OpenApiResponse(
                PydanticToDjangoSerializer.convert(ErrorResponse),
                description="토큰이 만료되거나 권한이 없을시 발생",
            ),
            503: OpenApiResponse(
                PydanticToDjangoSerializer.convert(ErrorResponse),
                description="기타 서버에러 발생시 발생",
            ),
        },
    )
    @validate_token(roles=UserRoles.USER_ROLES)
    @validate_query_params(QueryParams)
    def get(self, request, token_payload: UserTokenPayload, params: QueryParams):
        user_id = token_payload.user_id
        page = params.page
        page_size = params.page_size
        try:
            paged_result: PagedResult[
                IWorksheetRepo.WorksheetDTO
            ] = self.worksheet_use_case.bulk_fetch_process(
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

            return success_response(data=response_data, message="워크시트 조회에 성공했습니다.")

        except PagingException as e:
            return error_response(code=e.code, message=str(e), status=400)


class MYWorksheetView(APIView):
    """
    user 토큰을 까서 해당 유저의 worksheet 관련 view
    """

    class MainBlockSchema(BaseModel):
        block_type: str
        body: list

    class CreateBodyParams(BaseModel):
        name: str = Field(default="unknown", max_length=255)
        blocks: list
        main_block: dict
        raw_blocks: list
        raw_main_block: list

    class UpdateBodyParams(BaseModel):
        id: str
        name: str = Field(default="unknown", max_length=255)
        blocks: list
        main_block: dict
        raw_blocks: list
        raw_main_block: list

    def __init__(self):
        self.worksheet_use_case = WorksheetUseCase()

    @extend_schema(
        summary="worksheet fetch, id 를 넘겨줘서 가져온다.",
        description="",
        responses={
            201: OpenApiResponse(
                PydanticToDjangoSerializer.convert(SuccessResponse),
                description="성공적인 응답",
            ),
            400: OpenApiResponse(
                PydanticToDjangoSerializer.convert(ErrorResponse),
                description="worksheet not found error",
            ),
            403: OpenApiResponse(
                PydanticToDjangoSerializer.convert(ErrorResponse),
                description="토큰이 만료되거나 권한이 없을시 발생",
            ),
            503: OpenApiResponse(
                PydanticToDjangoSerializer.convert(ErrorResponse),
                description="기타 서버에러 발생시 발생",
            ),
        },
    )
    @validate_token(roles=UserRoles.USER_ROLES)
    def get(self, request, worksheet_id: str, token_payload: UserTokenPayload):
        """
        넘겨준 worksheet_id 에 해당되는 내용을 반환
        """
        try:
            worksheet = self.worksheet_use_case.fetch_process(worksheet_id=worksheet_id)

        except WorksheetException as e:
            return error_response(code=e.code, message=str(e), status=400)

        except FunctionException as e:
            return error_response(code=e.code, message=str(e), status=400)

        if worksheet.owner_id != token_payload.user_id:
            return error_response(
                code="DOES_NOT_PERMISSION",
                message="권한이 없습니다.",
                status=403,
                detail={"detail": "본인의 worksheet만 fetch 가능합니다."},
            )

        dicted_worksheet = worksheet.to_dict()
        return success_response(
            data=dicted_worksheet, message="성공적인 fetch올시다", status=200
        )

    @extend_schema(
        summary="worksheet 생성.",
        description="request는 뼈대만 보여줍니다. 실제 사용시에는 하단 스키마의  main_block, blocks을 참고한후 채워서 보내주세요.",
        request=PydanticToDjangoSerializer.convert(CreateBodyParams),
        responses={
            201: OpenApiResponse(
                PydanticToDjangoSerializer.convert(SuccessResponse),
                description="성공적인 응답",
            ),
            400: OpenApiResponse(
                PydanticToDjangoSerializer.convert(ErrorResponse),
                description="worksheet, function, block error",
            ),
            403: OpenApiResponse(
                PydanticToDjangoSerializer.convert(ErrorResponse),
                description="토큰이 만료되거나 권한이 없을시 발생",
            ),
            503: OpenApiResponse(
                PydanticToDjangoSerializer.convert(ErrorResponse),
                description="기타 서버에러 발생시 발생",
            ),
        },
    )
    @validate_token(roles=UserRoles.USER_ROLES)
    @validate_body(CreateBodyParams)
    def post(self, request, token_payload: UserTokenPayload, body: CreateBodyParams):
        """
        worksheet 생성.
        """

        try:
            main_block_vo = MainBlock.from_dict(body.main_block)
            blocks_vo = [Block.from_dict(block) for block in body.blocks]

        except (ValueError, AttributeError, KeyError) as e:
            return error_response(
                code="INVALID_BLOCK_FORMAT",
                message="invalid block format",
                detail={"invalid": str(e)},
                status=400,
            )

        try:
            worksheet_id = self.worksheet_use_case.create_process(
                worksheet_name=body.name,
                owner_id=token_payload.user_id,
                main_block=main_block_vo,  # vo
                blocks=blocks_vo,  # list[vo]
                raw_blocks=body.raw_blocks,
                raw_main_block=body.raw_main_block,
            )

            return success_response(
                data="", message=f"worksheet id {worksheet_id}가 생성되었소", status=201
            )

        except WorksheetException as e:
            return error_response(code=e.code, message=str(e), status=400)

        except FunctionException as e:
            return error_response(code=e.code, message=str(e), status=400)

    @extend_schema(
        summary="worksheet update.",
        description="request는 뼈대만 보여줍니다. 실제 사용시에는 하단 스키마의  main_block, blocks을 참고한후 채워서 보내주세요.",
        request=PydanticToDjangoSerializer.convert(UpdateBodyParams),
        responses={
            200: OpenApiResponse(
                PydanticToDjangoSerializer.convert(SuccessResponse),
                description="성공적인 응답",
            ),
            400: OpenApiResponse(
                PydanticToDjangoSerializer.convert(ErrorResponse),
                description="worksheet, function, block format error or 기타 에러",
            ),
            403: OpenApiResponse(
                PydanticToDjangoSerializer.convert(ErrorResponse),
                description="토큰이 만료되거나 권한이 없을시 발생",
            ),
            503: OpenApiResponse(
                PydanticToDjangoSerializer.convert(ErrorResponse),
                description="기타 서버에러 발생시 발생",
            ),
        },
    )
    @validate_token(roles=UserRoles.USER_ROLES)
    @validate_body(UpdateBodyParams)
    def put(
        self,
        request,
        worksheet_id: str,
        token_payload: UserTokenPayload,
        body: UpdateBodyParams,
    ):
        """
        worksheet id 에 해당되는 worksheet 를 수정한다.
        """
        worksheet = self.worksheet_use_case.fetch_process(worksheet_id=worksheet_id)
        if worksheet.owner_id != token_payload.user_id:
            return error_response(
                code="DOES_NOT_PERMISSION",
                message="권한이 없습니다.",
                status=403,
                detail={"detail": "본인의 worksheet만 수정 가능합니다."},
            )
        try:
            main_block_vo = MainBlock.from_dict(body.main_block)
            blocks_vo = [Block.from_dict(block) for block in body.blocks]

            self.worksheet_use_case.update_process(
                worksheet_id=worksheet_id,
                worksheet_name=body.name,
                owner_id=token_payload.user_id,
                main_block=main_block_vo,  # vo
                blocks=blocks_vo,  # list[vo]
                raw_blocks=body.raw_blocks,
                raw_main_block=body.raw_main_block,
            )

            return success_response(
                data="", message=f"worksheet id {worksheet_id}가 변경되었소", status=200
            )

        except (ValueError, AttributeError, KeyError) as e:
            return error_response(
                code="INVALID_BLOCK_FORMAT",
                message="invalid block format",
                detail={"invalid": str(e)},
                status=400,
            )

        except WorksheetException as e:
            return error_response(
                code=e.code, message=str(e), status=400, detail=e.detail
            )

        except FunctionException as e:
            return error_response(
                code=e.code, message=str(e), status=400, detail=e.detail
            )

    @extend_schema(
        summary="worksheet delete.",
        description="request는 뼈대만 보여줍니다. 실제 사용시에는 하단 스키마의  main_block, blocks을 참고한후 채워서 보내주세요.",
        responses={
            200: OpenApiResponse(
                PydanticToDjangoSerializer.convert(SuccessResponse),
                description="성공적인 응답",
            ),
            400: OpenApiResponse(
                PydanticToDjangoSerializer.convert(ErrorResponse),
                description="worksheet, function, block format error or 기타 에러",
            ),
            403: OpenApiResponse(
                PydanticToDjangoSerializer.convert(ErrorResponse),
                description="토큰이 만료되거나 권한이 없을시 발생",
            ),
            503: OpenApiResponse(
                PydanticToDjangoSerializer.convert(ErrorResponse),
                description="기타 서버에러 발생시 발생",
            ),
        },
    )
    @validate_token(roles=UserRoles.USER_ROLES)
    def delete(self, request, worksheet_id: str, token_payload: UserTokenPayload):
        """
        worksheet id 에 해당되는 worksheet 를 삭제한다.
        """
        try:
            worksheet = self.worksheet_use_case.fetch_process(worksheet_id=worksheet_id)
            if worksheet.owner_id != token_payload.user_id:
                return error_response(message="권한이 없습니다.")

            self.worksheet_use_case.delete_process(worksheet_id=worksheet_id)

        except WorksheetException as e:
            return error_response(
                code=e.code, detail=e.detail, message=str(e), status=400
            )

        except FunctionException as e:
            return error_response(
                code=e.code, message=str(e), status=400, detail=e.detail
            )

        except (ValueError, AttributeError, KeyError) as e:
            return error_response(
                code="INVALID_BLOCK_FORMAT",
                message="invalid block format",
                detail={"invalid": str(e)},
                status=400,
            )

        return success_response(
            data="", message=f"worksheet id {worksheet_id}가 삭제되었소", status=200
        )


class WorksheetValidatorView(APIView):
    def __init__(self, **kwargs: Any) -> None:
        self.worksheet_use_case = WorksheetUseCase()

    @dataclass
    class BodyParams(BaseModel):
        main_block: dict

    @extend_schema(
        summary="worksheet validate.",
        description="request는 뼈대만 보여줍니다. 실제 사용시에는 하단 스키마의  main_block, blocks을 참고한후 채워서 보내주세요.",
        request=PydanticToDjangoSerializer.convert(BodyParams),
        responses={
            200: OpenApiResponse(
                PydanticToDjangoSerializer.convert(SuccessResponse),
                description="성공적인 응답",
            ),
            400: OpenApiResponse(
                PydanticToDjangoSerializer.convert(ErrorResponse),
                description="worksheet, function, block format error",
            ),
            403: OpenApiResponse(
                PydanticToDjangoSerializer.convert(ErrorResponse),
                description="토큰이 만료되거나 권한이 없을시 발생",
            ),
            503: OpenApiResponse(
                PydanticToDjangoSerializer.convert(ErrorResponse),
                description="기타 서버에러 발생시 발생",
            ),
        },
    )
    @validate_token(roles=UserRoles.ALL_USER_ROLES)
    @validate_body(BodyParams)
    def post(self, request, token_payload: UserTokenPayload, body: BodyParams):
        try:
            main_block_vo = MainBlock.from_dict(body.main_block)

        except (ValueError, AttributeError, KeyError) as e:
            return error_response(
                code="INVALID_BLOCK_FORMAT",
                message="invalid block format",
                detail={"invalid": str(e)},
                status=400,
            )

        result = self.worksheet_use_case.validate_worksheet(main_block=main_block_vo)
        if result:
            data = {"target": result, "is_valid": False}
            return success_response(
                message="You are referencing a non-existent function.",
                status=200,
                data=data,
            )

        return success_response(data="", message="valid worksheet", status=200)
