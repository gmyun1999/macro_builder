import uuid

from common.domain import PagedResult
from common.service.paging import Paginator
from common.service.token.exception import InvalidPagingParameterException
from macro_sheet.domain.block.base_block.main_block import MainBlock
from macro_sheet.domain.block.block import Block
from macro_sheet.domain.worksheet.worksheet import Worksheet
from macro_sheet.service.exception.exceptions import (
    FunctionNotFoundException,
    NotLoggedInException,
    WorksheetException,
    WorksheetNotFoundException,
)
from macro_sheet.service.i_repo.i_worksheet_repo import IWorksheetRepo
from macro_sheet.service.service.block_function_service import BlockFunctionService
from macro_sheet.service.service.block_service import BlockService
from macro_sheet.service.service.worksheet_service import WorksheetService


class WorksheetUseCase:
    def __init__(self) -> None:
        self.worksheet_service = WorksheetService()
        self.block_function_service = BlockFunctionService()
        self.block_service = BlockService()

    def update_process(
        self,
        worksheet_id: str,
        worksheet_name: str,
        owner_id: str | None,
        main_block: MainBlock,
        blocks: list[Block],
        raw_blocks: list,
        raw_main_block: list,
    ) -> None:
        """
        사용자가 워크시트를 수정한 다음 저장할 때
        """
        # TODO: function_id 만 알면 쓸수있는데, permission을 걸어채워야할듯.

        if owner_id is None:
            raise NotLoggedInException()

        related_function = self.block_service.find_reference_blocks_in_block(
            block=main_block
        )

        related_function_ids = set()
        for func in related_function:
            related_function_ids.add(func["reference_id"])
            if not self.block_function_service.check_is_exist_id(func["reference_id"]):
                raise FunctionNotFoundException(func["reference_id"])

        worksheet = Worksheet(
            id=worksheet_id,
            name=worksheet_name,
            owner_id=owner_id,
            main_block=main_block,
            blocks=blocks,
            raw_blocks=raw_blocks,
            raw_main_block=raw_main_block,
        )

        self.worksheet_service.update_worksheet(
            worksheet_vo=worksheet, function_ids=list(related_function_ids)
        )

    def create_process(
        self,
        worksheet_name: str,
        owner_id: str | None,
        main_block: MainBlock | None,
        blocks: list[Block],
        raw_blocks: list,
        raw_main_block: list,
    ) -> str:
        """
        사용자가 처음 워크시트를 생성하고 저장할 때
        """
        # TODO: function_id 만 알면 쓸수있는데, permission을 걸어채워야할듯.
        if owner_id is None:
            raise NotLoggedInException()

        if main_block:
            related_function = self.block_service.find_reference_blocks_in_block(
                block=main_block
            )

            related_function_ids = set()
            for func in related_function:
                related_function_ids.add(func["reference_id"])
                if not self.block_function_service.check_is_exist_id(
                    func["reference_id"]
                ):
                    raise FunctionNotFoundException(func["reference_id"])

        worksheet_id = str(uuid.uuid4())
        worksheet = Worksheet(
            id=worksheet_id,
            name=worksheet_name,
            owner_id=owner_id,
            main_block=main_block if main_block is not None else None,
            blocks=blocks,
            raw_blocks=raw_blocks,
            raw_main_block=raw_main_block,
        )

        self.worksheet_service.create_worksheet_with_WorksheetFunction(
            worksheet_vo=worksheet, function_ids=list(related_function_ids)
        )

        return worksheet_id

    def delete_process(self, worksheet_id: str) -> None:
        """
        사용자가 기존의 워크시트를 삭제할 때
        """

        result = self.worksheet_service.delete_worksheet_with_WorksheetFunction(
            worksheet_id=worksheet_id
        )
        if not result:
            raise WorksheetNotFoundException(worksheet_id)

    def fetch_process(self, worksheet_id: str) -> IWorksheetRepo.WorksheetDTO:
        """
        사용자가 만들었던 워크시트를 불러올 때
        """
        result = self.worksheet_service.fetch_worksheet(worksheet_id=worksheet_id)
        if not result:
            raise WorksheetNotFoundException(worksheet_id)

        return result[0]

    def bulk_fetch_process(
        self, owner_id: str | None = None, page: int = 1, page_size: int = 10
    ) -> PagedResult[IWorksheetRepo.WorksheetDTO]:
        """
        사용자가 만든 모든 워크시트를 불러올 때
        """

        worksheets = self.worksheet_service.fetch_worksheet(owner_id=owner_id)
        paged_result = Paginator.paginate(
            items=worksheets, page=page, page_size=page_size
        )
        return paged_result

    def validate_worksheet(self, main_block: MainBlock) -> list[dict[str, str]]:
        # TODO: 현재는 main block은 따로 체크할게없음 나중에 syntax validate를 체크할떄 쓰이면 좋을듯
        reference_blocks = self.block_service.find_reference_blocks_in_block(
            block=main_block
        )
        not_exist_function_id = []

        for function in reference_blocks:
            # 일단은 존재하는지만 확인함
            is_exist = self.block_function_service.check_is_exist_id(
                function_id=function["reference_id"]
            )
            if not is_exist:
                not_exist_function_id.append(function)

        return not_exist_function_id
