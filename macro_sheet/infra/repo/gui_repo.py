from macro_sheet.domain.gui.gui import Gui as GuiVo
from macro_sheet.domain.gui.gui import Script as ScriptVo
from macro_sheet.infra.models import Gui, Script
from macro_sheet.service.i_repo.i_gui_repo import IGuiRepo, IScriptRepo


class GuiRepo(IGuiRepo):
    def create(self, gui_vo: GuiVo) -> GuiVo:
        """
        gui를 생성하고 관련 데이터를 저장한다
        """
        gui_model = Gui(
            id=gui_vo.id,
            name=gui_vo.name,
            url=gui_vo.url,
        )
        gui_model.save()
        return gui_vo

    def fetch(self, filter: IGuiRepo.Filter) -> list[GuiVo]:
        """
        gui의 정보를 가져온다
        """
        query = Gui.objects.all()

        if filter.id:
            query = query.filter(id=filter.id)

        gui_models = query.all()
        gui_vos = [
            GuiVo(id=str(gui_model.id), name=gui_model.name, url=gui_model.url)
            for gui_model in gui_models
        ]
        return gui_vos

    def update(self, gui_vo: GuiVo) -> GuiVo:
        """
        gui의 정보를 업데이트한다
        """
        try:
            gui_model = Gui.objects.get(id=gui_vo.id)
            gui_model.name = gui_vo.name
            gui_model.url = gui_vo.url
            gui_model.save()
            return gui_vo

        except Gui.DoesNotExist:
            raise Exception("Gui not found")

    def delete(self, gui_id: str) -> None:
        """
        gui의 정보를 삭제한다.
        """
        try:
            gui_model = Gui.objects.get(id=gui_id)
            gui_model.delete()
        except Gui.DoesNotExist:
            raise Exception("Gui not found")


class ScriptRepo(IScriptRepo):
    def get(self, filter: IScriptRepo.Filter) -> ScriptVo | None:
        queryset = Script.objects.all()

        if filter.id:
            queryset = queryset.filter(id=filter.id)
        if filter.script_hash:
            queryset = queryset.filter(script_hash=filter.script_hash)
        if filter.gui_id:
            queryset = queryset.filter(gui_id=filter.gui_id)

        try:
            script_model = queryset.get()
            return ScriptVo(
                id=script_model.id,
                script_code=script_model.script_code,
                script_hash=script_model.script_hash,
                gui_id=script_model.gui_id,
            )
        except Script.DoesNotExist:
            return None

    def create(self, script: ScriptVo) -> ScriptVo:
        script_model = Script.objects.create(
            id=script.id,
            script_code=script.script_code,
            script_hash=script.script_hash,
            gui_id=script.gui_id,
        )
        return ScriptVo(
            id=script_model.id,
            script_code=script_model.script_code,
            script_hash=script_model.script_hash,
            gui_id=script_model.gui_id,
        )

    def delete(self, script_id: str) -> bool:
        try:
            script_model = Script.objects.get(id=script_id)
            script_model.delete()
            return True
        except Script.DoesNotExist:
            return False

    def get_or_create_by_hash(self, script: ScriptVo) -> ScriptVo:
        # script_hash로 먼저 기존 객체 조회
        try:
            existing_script = Script.objects.get(script_hash=script.script_hash)
            return ScriptVo(
                id=existing_script.id,
                script_code=existing_script.script_code,
                script_hash=existing_script.script_hash,
                gui_id=existing_script.gui_id,
            )
        except Script.DoesNotExist:
            # 동일한 해시가 없으면 새로 생성
            return self.create(script)

    def is_same_script_code(self, script_hash: str) -> bool:
        """
        주어진 ScriptVo와 동일한 script_code를 가진 Script가 존재하는지 확인합니다.
        존재하면 True를 반환하고, 존재하지 않으면 False를 반환합니다.
        """
        return Script.objects.filter(script_hash=script_hash).exists()
