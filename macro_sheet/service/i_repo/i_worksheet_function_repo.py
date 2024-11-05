from abc import ABC, abstractmethod


class IWorksheetFunctionRepo(ABC):
    class WorksheetFunctionVo:
        def __init__(self, worksheet_id: str, function_id: str):
            self.worksheet_id = worksheet_id
            self.function_id = function_id

    @abstractmethod
    def bulk_create_worksheet_functions(
        self, worksheet_functions: list[WorksheetFunctionVo]
    ) -> None:
        """WorksheetFunction 객체들을 일괄 생성한다"""
        pass

    @abstractmethod
    def delete_worksheet_functions_by_worksheet_id(self, worksheet_id: str) -> None:
        """특정 worksheet_id에 해당하는 WorksheetFunction 데이터를 삭제한다"""
        pass
