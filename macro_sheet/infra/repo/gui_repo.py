from macro_sheet.domain.gui.gui import Gui as GuiVo
from macro_sheet.infra.models import Gui
from macro_sheet.service.i_repo.i_gui_repo import IGuiRepo


class GuiRepo(IGuiRepo):
    def create(self, gui_vo: GuiVo) -> GuiVo:
        """
        gui를 생성하고 관련 데이터를 저장한다
        """
        gui_model = Gui(
            id=gui_vo.id,
            name=gui_vo.name,
            owner_id=gui_vo.owner_id,
            worksheet_id=gui_vo.worksheet_id,
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
        if filter.owner_id:
            query = query.filter(owner_id=filter.owner_id)
        if filter.worksheet_id:
            query = query.filter(worksheet_id=filter.worksheet_id)

        gui_models = query.all()
        gui_vos = [
            GuiVo(
                id=str(gui_model.id),
                name=gui_model.name,
                owner_id=str(gui_model.owner_id) if gui_model.owner_id else None,
                worksheet_id=str(gui_model.worksheet_id)
                if gui_model.worksheet_id
                else None,
                url=gui_model.url,
            )
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
            gui_model.owner_id = gui_vo.owner_id
            gui_model.worksheet_id = gui_vo.worksheet_id
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
