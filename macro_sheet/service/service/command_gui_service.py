import hashlib

from django.db import transaction

from macro_sheet.domain.gui.gui import Gui, Script
from macro_sheet.infra.packing_server import PackagingClient
from macro_sheet.infra.repo.gui_repo import GuiRepo, ScriptRepo
from macro_sheet.service.i_packaging_server.i_packaging_server import (
    PackagingClientInterface,
)
from macro_sheet.service.i_repo.i_gui_repo import IGuiRepo, IScriptRepo


class CommandGuiService:
    def __init__(self) -> None:
        # TODO: DI
        self.client: PackagingClientInterface = PackagingClient()
        self.gui_repo: IGuiRepo = GuiRepo()
        self.script_repo: IScriptRepo = ScriptRepo()

    def get_gui_link(self, script_code: str) -> str:
        """
        script code를 로컬에 저장하는건 아닌거같고,
        어떤 형태로 해서 바로 패키지 서버로 보낸다음
        패키지 서버로부터 s3 link를 받는다.
        """
        download_url = self.client.get_gui_link(script_content=script_code)
        return download_url

    def create_script_hash_by_code(self, script_code: str) -> str:
        """
        code로 script hash 반환
        """
        return hashlib.sha256(script_code.encode("utf-8")).hexdigest()

    def is_same_script_code(self, script_code: str) -> bool:
        script_hash = self.create_script_hash_by_code(script_code=script_code)
        return self.script_repo.is_same_script_code(script_hash=script_hash)

    def save_script(self, script: Script):
        """
        script save
        """
        return self.script_repo.create(script=script)

    def get_script_by_hash(self, script_hash: str) -> Script | None:
        return self.script_repo.get(self.script_repo.Filter(script_hash=script_hash))

    def save_gui(self, gui: Gui):
        """
        gui link를 받아서 저장하는거. 모델이 필요할듯.
        """
        return self.gui_repo.create(gui_vo=gui)

    def get_gui_by_id(self, gui_id: str) -> Gui | None:
        gui_vo = self.gui_repo.fetch(self.gui_repo.Filter(id=gui_id))
        if not gui_id:
            return None

        return gui_vo[0]

    def save_gui_and_script(self, gui: Gui, script: Script):
        with transaction.atomic():
            self.save_gui(gui=gui)
            self.save_script(script=script)

    def delete_gui(self, gui: Gui):
        """
        gui 삭제
        """
        pass

    def modify_gui(
        self,
    ):
        """
        변경같은거없음 기존꺼 지우고 다시 s3에 올리는건데, 굳이? 그냥 냅두고싶음
        """
        pass
