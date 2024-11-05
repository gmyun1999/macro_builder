from django.db import transaction

from macro_sheet.domain.worksheet import Worksheet as WorksheetVo
from macro_sheet.infra.repo.worksheet_function_repo import WorksheetFunctionRepo
from macro_sheet.infra.repo.worksheet_repo import WorksheetRepo
from macro_sheet.service.i_repo.i_worksheet_function_repo import IWorksheetFunctionRepo
from macro_sheet.service.i_repo.i_worksheet_repo import IWorksheetRepo


class WorksheetService:
    def __init__(self) -> None:
        self.worksheet_repo: IWorksheetRepo = WorksheetRepo()  # 의존성 주입
        self.worksheet_function_repo: IWorksheetFunctionRepo = (
            WorksheetFunctionRepo()
        )  # 의존성 주입

    @transaction.atomic
    def create_worksheet_with_WorksheetFunction(
        self, worksheet_vo: WorksheetVo, function_ids: list[str] | None = None
    ) -> WorksheetVo:
        # Worksheet 생성
        created_worksheet = self.worksheet_repo.create_worksheet(worksheet_vo)

        # function_ids가 있는 경우 WorksheetFunction을 bulk로 생성
        if function_ids:
            worksheet_functions = [
                IWorksheetFunctionRepo.WorksheetFunctionVo(
                    worksheet_id=created_worksheet.id, function_id=function_id
                )
                for function_id in function_ids
            ]
            self.worksheet_function_repo.bulk_create_worksheet_functions(
                worksheet_functions
            )

        return created_worksheet

    @transaction.atomic
    def update_worksheet(
        self, worksheet_vo: WorksheetVo, function_ids: list[str] | None = None
    ) -> WorksheetVo:
        # 기존 Worksheet 업데이트
        updated_worksheet = self.worksheet_repo.update_worksheet(worksheet_vo)

        # 기존 WorksheetFunction 데이터 삭제
        self.worksheet_function_repo.delete_worksheet_functions_by_worksheet_id(
            updated_worksheet.id
        )

        # 변경된 function_ids로 WorksheetFunction을 bulk로 생성
        if function_ids:
            worksheet_functions = [
                IWorksheetFunctionRepo.WorksheetFunctionVo(
                    worksheet_id=updated_worksheet.id, function_id=function_id
                )
                for function_id in function_ids
            ]
            self.worksheet_function_repo.bulk_create_worksheet_functions(
                worksheet_functions
            )

        return updated_worksheet

    @transaction.atomic
    def delete_worksheet_with_WorksheetFunction(
        self, worksheet_vo: WorksheetVo
    ) -> bool:
        # WorksheetFunction 데이터 삭제
        self.worksheet_function_repo.delete_worksheet_functions_by_worksheet_id(
            worksheet_vo.id
        )

        # Worksheet 삭제
        return self.worksheet_repo.delete_worksheet(worksheet_vo)

    def fetch_worksheet(self, worksheet_id: str) -> WorksheetVo | None:
        filter_obj = IWorksheetRepo.Filter(id=worksheet_id)

        worksheets = self.worksheet_repo.fetch_worksheet(filter_obj)
        return worksheets[0] if worksheets else None
