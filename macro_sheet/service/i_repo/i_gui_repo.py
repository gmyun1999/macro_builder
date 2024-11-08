from abc import ABC, abstractmethod

from macro_sheet.domain.gui.gui import Gui as GuiVo


class IGuiRepo(ABC):
    class Filter:
        def __init__(
            self,
            id: str | None = None,
            owner_id: str | None = None,
            worksheet_id: str | None = None,
        ) -> None:
            self.id = id
            self.owner_id = owner_id
            self.worksheet_id = worksheet_id

    @abstractmethod
    def create(self, gui_vo: GuiVo) -> GuiVo:
        """
        gui 를 생성하고 관련 데이터를 저장한다
        """
        pass

    @abstractmethod
    def fetch(self, filter: Filter) -> list[GuiVo]:
        """
        gui의 정보를 가져온다
        """
        pass

    @abstractmethod
    def update(self, gui_vo: GuiVo) -> GuiVo:
        """
        gui의 정보를 업데이트한다
        """
        pass

    @abstractmethod
    def delete(self, gui_id: str):
        """
        gui의 정보를 삭제한다.
        """
        pass
