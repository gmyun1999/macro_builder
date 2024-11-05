from macro_sheet.infra.models import WorksheetFunction
from macro_sheet.service.i_repo.i_worksheet_function_repo import IWorksheetFunctionRepo


class WorksheetFunctionRepo(IWorksheetFunctionRepo):
    def bulk_create_worksheet_functions(
        self, worksheet_functions: list[IWorksheetFunctionRepo.WorksheetFunctionVo]
    ) -> None:
        # 도메인 객체를 모델 객체로 변환 후 bulk_create 수행
        worksheet_function_objs = [
            WorksheetFunction(
                worksheet_id=wf_vo.worksheet_id, function_id=wf_vo.function_id
            )
            for wf_vo in worksheet_functions
        ]
        WorksheetFunction.objects.bulk_create(worksheet_function_objs)

    def delete_worksheet_functions_by_worksheet_id(self, worksheet_id: str) -> None:
        WorksheetFunction.objects.filter(worksheet_id=worksheet_id).delete()
