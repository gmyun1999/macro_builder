import hashlib

from django.db import transaction

from macro_sheet.domain.gui.gui import Gui, Script
from macro_sheet.infra.packing_server import PackagingServer
from macro_sheet.infra.pyqt_command_gui_server import PyQtCommandGuiServer
from macro_sheet.infra.repo.gui_repo import GuiRepo, ScriptRepo
from macro_sheet.service.i_command_gui_server.i_command_gui_server import (
    ICommandGuiServer,
)
from macro_sheet.service.i_packaging_server.i_packaging_server import IPackagingServer
from macro_sheet.service.i_repo.i_gui_repo import IGuiRepo, IScriptRepo


class CommandGuiService:
    def __init__(self) -> None:
        # TODO: DI
        self.client: IPackagingServer = PackagingServer()
        self.gui_repo: IGuiRepo = GuiRepo()
        self.script_repo: IScriptRepo = ScriptRepo()
        self.command_gui_service: ICommandGuiServer = PyQtCommandGuiServer()

    """============================================================================================"""
    """================================ packaging 서버 관련(under) ================================="""
    """============================================================================================"""

    def get_packaged_gui_download_link_from_packaging_server(
        self, script_code: str
    ) -> str:
        """
        packaging 서버로 부터 script code를 넘겨서
        packaging된 폴더의 link를 받아온다.
        """
        download_url = self.client.get_packaged_download_link(
            script_content=script_code
        )
        return download_url

    """============================================================================================"""
    """================================ gui, gui_script 엔티티 관련(under) ========================="""
    """============================================================================================"""

    def create_script_hash_by_code(self, script_code: str) -> str:
        """
        code로 script hash 반환
        """
        return hashlib.sha256(script_code.encode("utf-8")).hexdigest()

    def is_same_script_code(self, script_code: str) -> bool:
        """
        command_gui에서 동작하는 script_code가 이미 존재하는지 확인
        """
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
        gui link를 받아서 저장하는거
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
