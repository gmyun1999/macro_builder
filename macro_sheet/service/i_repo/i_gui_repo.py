from abc import ABC, abstractmethod

from macro_sheet.domain.gui.gui import Gui as GuiVo
from macro_sheet.domain.gui.gui import Script as ScriptVo


class IGuiRepo(ABC):
    class Filter:
        def __init__(
            self,
            id: str | None = None,
        ) -> None:
            self.id = id

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


class IScriptRepo:
    class Filter:
        def __init__(
            self,
            script_hash: str | None = None,
            id: str | None = None,
            gui_id: str | None = None,
        ):
            self.script_hash = script_hash
            self.id = id
            self.gui_id = gui_id

    @abstractmethod
    def get(self, filter: Filter) -> ScriptVo | None:
        pass

    @abstractmethod
    def create(self, script: ScriptVo):
        pass

    @abstractmethod
    def delete(self, script_id: str):
        pass

    @abstractmethod
    def get_or_create_by_hash(self, script: ScriptVo) -> ScriptVo:
        pass

    @abstractmethod
    def is_same_script_code(self, script_hash: str) -> bool:
        pass
