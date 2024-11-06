from macro_sheet.infra.packing_server import PackagingClient
from macro_sheet.service.i_packaging_server.i_packaging_server import (
    PackagingClientInterface,
)


class GuiService:
    def __init__(self) -> None:
        # TODO: DI
        self.client: PackagingClientInterface = PackagingClient()

    def get_gui_link(self, script_code):
        """
        script code를 로컬에 저장하는건 아닌거같고,
        어떤 형태로 해서 바로 패키지 서버로 보낸다음
        패키지 서버로부터 s3 link를 받는다.
        """
        pass

    def save_gui_link(
        self,
    ):
        """
        gui link를 받아서 저장하는거. 모델이 필요할듯.
        """
        pass

    def delete_gui(
        self,
    ):
        """
        gui의 link에 해당되는 데이터를 s3 에서 지운다.
        """
        pass

    def modify_gui(
        self,
    ):
        """
        변경같은거없음 기존꺼 지우고 다시 s3에 올리는건데, 굳이? 그냥 냅두고싶음
        """
        pass
