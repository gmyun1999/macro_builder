import uuid

from common.domain import PagedResult
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
from macro_sheet.service.service.worksheet_service import WorksheetService


class WorksheetUseCase:
    def __init__(self) -> None:
        self.worksheet_service = WorksheetService()
        self.block_function_service = BlockFunctionService()

    def update_process(
        self,
        worksheet_id: str,
        worksheet_name: str,
        owner_id: str | None,
        main_block: MainBlock,
        blocks: list[Block],
        related_function_ids: list[str] | None,
        raw_blocks: list,
        raw_main_block: list,
    ) -> None:
        """
        사용자가 워크시트를 수정한 다음 저장할 때
        """
        if owner_id is None:
            raise NotLoggedInException()

        if related_function_ids:
            for func_id in related_function_ids:
                if not self.block_function_service.check_is_exist_id(func_id):
                    raise FunctionNotFoundException(func_id)

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
            worksheet_vo=worksheet, function_ids=related_function_ids
        )

    def create_process(
        self,
        worksheet_name: str,
        owner_id: str | None,
        main_block: MainBlock | None,
        blocks: list[Block],
        related_function_ids: list[str] | None,
        raw_blocks: list,
        raw_main_block: list,
    ) -> str:
        """
        사용자가 처음 워크시트를 생성하고 저장할 때
        """
        if owner_id is None:
            raise NotLoggedInException()

        if related_function_ids:
            for func_id in related_function_ids:
                if not self.block_function_service.check_is_exist_id(func_id):
                    raise FunctionNotFoundException(func_id)

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
            worksheet_vo=worksheet, function_ids=related_function_ids
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
        if page < 1 or page_size < 1:
            raise InvalidPagingParameterException("페이지 번호와 페이지 크기는 1 이상이어야 합니다.")

        MAX_PAGE_SIZE = 100
        if page_size > MAX_PAGE_SIZE:
            raise InvalidPagingParameterException(
                f"페이지 크기는 최대 {MAX_PAGE_SIZE}까지 가능합니다."
            )

        worksheets = self.worksheet_service.fetch_worksheet(owner_id=owner_id)
        print(worksheets[0].id)
        print(worksheets[0].owner_id)
        print(worksheets[0].main_block)
        total_items = len(worksheets)
        total_pages = (total_items + page_size - 1) // page_size if page_size > 0 else 0

        # 페이지 번호가 총 페이지 수를 초과하는 경우
        if page > total_pages and total_pages != 0:
            raise InvalidPagingParameterException("페이지 번호가 총 페이지 수를 초과합니다.")

        # 페이징 처리
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        paged_items = worksheets[start_index:end_index]
        print(paged_items)
        return PagedResult(
            items=paged_items,
            total_items=total_items,
            total_pages=total_pages,
            current_page=page,
            page_size=page_size,
            has_previous=(page > 1),
            has_next=(page < total_pages),
        )
