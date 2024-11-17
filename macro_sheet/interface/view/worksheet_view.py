from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel, Field
from rest_framework.views import APIView

from common.domain import PagedResult
from common.interface.response import error_response, success_response
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
            if hasattr(e, "code"):
                return error_response(code=e.code, message=str(e), status=400)
            else:
                return error_response(code="UNKNOWN_ERROR", message=str(e), status=400)


class MYWorksheetView(APIView):
    """
    user 토큰을 까서 해당 유저의 worksheet 관련 view
    """

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
            return error_response(message="권한이 없습니다.")

        dicted_worksheet = worksheet.to_dict()
        return success_response(
            data=dicted_worksheet, message="성공적인 fetch올시다", status=200
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

        except (ValueError, AttributeError) as e:
            return error_response(message="유효하지 않은 블록 형식입니다.", status=400)

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
        try:
            worksheet = self.worksheet_use_case.fetch_process(worksheet_id=worksheet_id)
            if worksheet.owner_id != token_payload.user_id:
                return error_response(message="권한이 없습니다.")

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
        except WorksheetException as e:
            return error_response(
                code=e.code, message=str(e), status=400, detail=e.detail
            )

        except FunctionException as e:
            return error_response(
                code=e.code, message=str(e), status=400, detail=e.detail
            )

        except (ValueError, AttributeError) as e:
            return error_response(message="유효하지 않은 블록 형식입니다.", status=400)

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

        except (ValueError, AttributeError) as e:
            return error_response(message="유효하지 않은 블록 형식입니다.", status=400)

        return success_response(
            data="", message=f"worksheet id {worksheet_id}가 삭제되었소", status=200
        )


class WorksheetValidatorView(APIView):
    def __init__(self, **kwargs: Any) -> None:
        self.worksheet_use_case = WorksheetUseCase()

    @dataclass
    class BodyParams(BaseModel):
        main_block: dict

    @validate_token(roles=UserRoles.ALL_USER_ROLES)
    @validate_body(BodyParams)
    def post(self, request, token_payload: UserTokenPayload, body: BodyParams):
        try:
            main_block_vo = MainBlock.from_dict(body.main_block)

        except (ValueError, AttributeError) as e:
            return error_response(message="유효하지 않은 블록 형식입니다.", status=400)

        result = self.worksheet_use_case.validate_worksheet(main_block=main_block_vo)
        if result:
            data = {"target": result, "is_valid": False}
            return success_response(
                message=f"존재하지않는 function을 참조하고있습니다", status=200, data=data
            )

        return success_response(
            data={"target": result, "is_valid": True}, message=f"valid", status=200
        )
