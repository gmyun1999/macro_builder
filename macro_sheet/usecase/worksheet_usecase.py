import uuid

from macro_sheet.domain.block.block import Block
from macro_sheet.domain.worksheet.worksheet import Worksheet
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
        main_blocks: list[Block | None],
        blocks: list[Block | None],
        related_function_ids: list[str] | None,
    ) -> tuple[bool, str]:
        """
        사용자가 워크시트를 수정한다음 저장핳때
        """

        if owner_id is None:
            return False, "로그인을 하지않으면 저장이 불가능함"

        worksheet = Worksheet(
            id=worksheet_id,
            name=worksheet_name,
            owner_id=owner_id,
            main_blocks=main_blocks,
            blocks=blocks,
        )
        self.worksheet_service.update_worksheet(
            worksheet_vo=worksheet, function_ids=related_function_ids
        )

        return True, ""

    def create_process(
        self,
        worksheet_name: str,
        owner_id: str | None,
        main_blocks: list[Block | None],
        blocks: list[Block | None],
        related_function_ids: list[str] | None,
    ) -> tuple[bool, str]:
        """
        사용자가 처음 워크시트를 생성하고 저장할떄
        """

        if owner_id is None:
            return False, "로그인을 하지않으면 저장이 불가능함"

        worksheet = Worksheet(
            id=str(uuid.uuid4()),
            name=worksheet_name,
            owner_id=owner_id,
            main_blocks=main_blocks,
            blocks=blocks,
        )
        self.worksheet_service.create_worksheet_with_WorksheetFunction(
            worksheet_vo=worksheet, function_ids=related_function_ids
        )

        return True, ""

    def delete_process(self, worksheet_id) -> tuple[bool, str]:
        """
        사용자가 기존의 워크시트를 삭제할때
        """
        result = self.worksheet_service.delete_worksheet_with_WorksheetFunction(
            worksheet_id=worksheet_id
        )
        return result, ""

    def fetch_process(
        self, worksheet_id: str
    ) -> tuple[IWorksheetRepo.WorksheetDTO | None, str]:
        """
        사용자가 만들었던 워크시트를 불러올때
        """

        result = self.worksheet_service.fetch_worksheet(worksheet_id=worksheet_id)
        if result is None:
            return None, "해당되는 워크시트 없음"

        return result[0], ""

    def bulk_fetch_process(
        self, owner_id: str
    ) -> tuple[list[IWorksheetRepo.WorksheetDTO] | None, str]:
        """
        사용자가 만든 모든 워크시트를 불러올때
        """
        result = self.worksheet_service.fetch_worksheet(owner_id=owner_id)

        if result is None:
            return None, "만든 워크시트가없음"

        return result, ""
