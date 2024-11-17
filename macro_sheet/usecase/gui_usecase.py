import uuid

from macro_sheet.domain.block.base_block.main_block import MainBlock
from macro_sheet.domain.block.block import Block
from macro_sheet.domain.Function.block_function import BlockFunction
from macro_sheet.domain.gui.gui import Gui, Script
from macro_sheet.domain.worksheet.worksheet import Worksheet as WorksheetVo
from macro_sheet.service.exception.exceptions import (
    FunctionNotFoundException,
    MainBlockEmptyException,
)
from macro_sheet.service.service.block_function_service import BlockFunctionService
from macro_sheet.service.service.block_service import BlockService
from macro_sheet.service.service.gui_service import GuiService


class GuiUseCase:
    def __init__(self) -> None:
        self.gui_service = GuiService()
        self.block_service = BlockService()
        self.block_function_service = BlockFunctionService()

    def generate_gui(
        self,
        owner_id: str | None,
        main_block: MainBlock | None,
    ) -> str:
        """
        *reference block에 해당되는 function이 실제로 없으면 이미 삭제된 function을
        *참조하는 reference block이 껴있는거임.

        gui 생성하기 버튼 눌렀을떄 발생하는일임
        <조건> related_function_ids가 존재하는지 체크 -> 없으면 반환.
        변환하기전에 function이랑 block 관련된 체크를 모두해야함
        일단 script 코드로 변환함.

        <조건>script 코드를 보내기전에 동일한 script가 존재하는지 확인해야함. 만약 동일한 스크립트라면 보낼필요없이
        해당 script의 gui_id 를 가지고 s3에서 fetch 하면됨.
        <일반>script 코드를 가지고 서버에 보내야함.
        서버에 보냈다는거는
        s3에 올라갔다는거니깐 다운로드 링크 가지고와서 fetch 하면됨.
        이때 fetch 한 이후에 gui도 저장하고 script도 저장해야함.
        """

        full_ancestors: set[BlockFunction] = set()
        if not main_block:
            raise MainBlockEmptyException()

        related_function = self.block_service.find_reference_blocks_in_block(
            block=main_block
        )
        for func in related_function:
            func_id = func["reference_id"]
            if not self.block_function_service.check_is_exist_id(func_id):
                raise FunctionNotFoundException(func_id)
            # TODO: 여러개의 func_id 넘겨줫을때 중복 제거하고 한번에 모든 조상 다가져오는 repo 만들기
            ancestors_ids = self.block_function_service.get_ancestors_ids(
                function_id=func_id
            )
            for id in ancestors_ids:
                block_function_vo = self.block_function_service.fetch_function_by_id(
                    function_id=id
                )
                if block_function_vo is not None:
                    full_ancestors.add(block_function_vo)

        script_code = self.block_service.generate_script_from_worksheet(
            main_block=main_block, block_functions=list(full_ancestors)
        )

        script_hash = self.gui_service.create_script_hash_by_code(
            script_code=script_code
        )
        script_vo = self.gui_service.get_script_by_hash(script_hash=script_hash)
        if script_vo:
            # 이미 존재하는 스크립트 이므로 관련 gui도 존재함. 왜냐면 gui와 스크립트는 같이 삭제되고 같이 생성됨
            # 따라서 패키징 하지않고 바로 gui data를 가져와서 link를 전달한다.
            gui_vo = self.gui_service.get_gui_by_id(script_vo.gui_id)
            download_link = gui_vo.url  # type: ignore
            return download_link

        # 스크립트가 존재하지않으면 이 스크립트를 가지고와서 패키징 서버에 밀어넣은후에 s3 gui link ,script 모두 저장해야한다.
        download_link = self.gui_service.get_gui_link(script_code=script_code)

        gui_vo = Gui(
            id=str(uuid.uuid4()),
            name=str(uuid.uuid4()),
            url=download_link,
        )
        script_vo = Script(
            id=str(uuid.uuid4()),
            script_code=script_code,
            gui_id=gui_vo.id,
            script_hash=script_hash,
        )
        self.gui_service.save_gui_and_script(script=script_vo, gui=gui_vo)

        return download_link
