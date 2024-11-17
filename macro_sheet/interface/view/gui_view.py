from dataclasses import dataclass
from typing import Any

from django.http import JsonResponse
from pydantic import BaseModel, Field
from rest_framework import status
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
from macro_sheet.usecase.gui_usecase import GuiUseCase
from macro_sheet.usecase.worksheet_usecase import WorksheetUseCase
from user.domain.user_role import UserRoles
from user.domain.user_token import UserTokenPayload
from user.interface.validator.user_token_validator import validate_token


class GenerateGuiView:
    def __init__(self) -> None:
        self.gui_use_case = GuiUseCase()

    class GuiCreateParam(BaseModel):
        name: str = Field(default="unknown", max_length=255)
        blocks: list
        main_block: dict
        raw_blocks: list
        raw_main_block: list

    @validate_token(roles=UserRoles.USER_ROLES)
    @validate_body(GuiCreateParam)
    def post(
        self,
        request,
        token_payload: UserTokenPayload,
        body: GuiCreateParam,
    ):
        """
        gui 를 생성하고 다운로드 link 를 넘겨준다.
        """
        # self.gui_use_case.
        pass
