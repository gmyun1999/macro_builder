from abc import ABC, abstractmethod

from macro_sheet.domain.worksheet.worksheet import Worksheet as WorksheetVo


class IWorksheetRepo(ABC):
    class Filter:
        def __init__(self, id: str | None = None, owner_id: str | None = None):
            self.id = id
            self.owner_id = owner_id

    class WorksheetDTO:
        def __init__(
            self,
            id: str,
            name: str,
            owner_id: str | None,
            main_block: dict | None,
            blocks: list[dict | None],
        ):
            self.id = id
            self.name = name
            self.owner_id = owner_id
            self.main_block = main_block
            self.blocks = blocks

    @abstractmethod
    def fetch_worksheet(self, filter: Filter) -> list[WorksheetDTO]:
        """
        filter 조건에 맞는 worksheet 가져오기
        """
        pass

    @abstractmethod
    def create_worksheet(self, Worksheet_obj: WorksheetVo) -> WorksheetDTO:
        """
        worksheet 생성
        """
        pass

    @abstractmethod
    def update_worksheet(self, Worksheet_obj: WorksheetVo) -> WorksheetDTO:
        """
        기존 worksheet 수정
        """
        pass

    @abstractmethod
    def delete_worksheet(self, worksheet_id: str) -> bool:
        """s
        function 삭제
        """
        pass
