import logging

from pydantic import BaseModel, Field
from rest_framework.views import APIView

from common.interface.response import error_response, success_response
from common.interface.validators import validate_body
from macro_sheet.domain.block.base_block.main_block import MainBlock
from macro_sheet.service.exception.exceptions import (
    DownloadLinkNotFoundException,
    FunctionException,
    RecorderStorageException,
)
from macro_sheet.usecase.gui_usecase import GuiUseCase
from user.domain.user_role import UserRoles
from user.domain.user_token import UserTokenPayload
from user.interface.validator.user_token_validator import validate_token

logger = logging.getLogger(__name__)


class GenerateCommandGuiView(APIView):
    def __init__(self) -> None:
        self.gui_use_case = GuiUseCase()

    class GuiCreateParam(BaseModel):
        name: str = Field(default="unknown", max_length=255)
        main_block: dict

    @validate_token(roles=UserRoles.ALL_USER_ROLES)
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
        if token_payload.user_id:
            owner_id = token_payload.user_id
        if token_payload.guest_id:
            owner_id = token_payload.guest_id

        try:
            dicted_main_block = MainBlock.from_dict(body.main_block)
        except (ValueError, AttributeError) as e:
            return error_response(
                detail={"detail": str(e)}, message="유효하지 않은 블록 형식입니다.", status=400
            )

        try:
            download_link = self.gui_use_case.generate_command_gui(
                owner_id=owner_id, main_block=dicted_main_block
            )
            data = {"download_link": download_link}
            return success_response(
                data=data, message="성공적으로 gui를 생성하였습니다.", status=200
            )
        except DownloadLinkNotFoundException as e:
            logger.error("Download link not found: %s", e, exc_info=True)
            return error_response(code=e.code, message=str(e), status=503)

        except FunctionException as e:
            return error_response(
                code=e.code, message=str(e), detail=e.detail, status=400
            )


class GenerateRecorderGuiView(APIView):
    def __init__(self) -> None:
        self.gui_use_case = GuiUseCase()

    @validate_token(roles=UserRoles.ALL_USER_ROLES)
    def get(self, request, token_payload: UserTokenPayload):
        """
        recorder gui 를 생성하고 다운로드 link 를 넘겨준다.
        """
        if token_payload.user_id:
            owner_id = token_payload.user_id
        if token_payload.guest_id:
            owner_id = token_payload.guest_id

        try:
            pre_signed_url = self.gui_use_case.get_recorder_gui_presigned_url()
            data = {"pre_signed_url": pre_signed_url}

            return success_response(
                data=data,
                message="성공적으로 recorder gui 링크를 반환하였습니다. 유효기간은 5분입니다.",
                status=200,
            )

        except RecorderStorageException as e:
            return error_response(code=e.code, message=str(e), status=503)
