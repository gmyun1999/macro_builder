from abc import ABC, abstractmethod

from macro_sheet.domain.worksheet.worksheet import Worksheet as WorksheetVo


class IWorksheetRepo(ABC):
    class Filter:
        def __init__(self, id: str | None = None, owner_id: str | None = None):
            self.id = id
            self.owner_id = owner_id

    @abstractmethod
    def fetch_worksheet(self, filter: Filter) -> list[WorksheetVo]:
        """
        filter 조건에 맞는 worksheet 가져오기
        """
        pass

    @abstractmethod
    def create_worksheet(self, Worksheet_obj: WorksheetVo) -> WorksheetVo:
        """
        worksheet 생성
        """
        pass

    @abstractmethod
    def update_worksheet(self, Worksheet_obj: WorksheetVo) -> WorksheetVo:
        """
        기존 worksheet 수정
        """
        pass

    @abstractmethod
    def delete_worksheet(self, Worksheet_obj: WorksheetVo) -> bool:
        """
        function 삭제
        """
        pass

    @abstractmethod
    def bulk_create_worksheets(
        self, worksheets: list[WorksheetVo]
    ) -> list[WorksheetVo]:
        """여러 Worksheet를 일괄 생성"""
        pass
