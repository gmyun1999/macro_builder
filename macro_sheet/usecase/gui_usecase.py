from macro_sheet.domain.block.block import Block


class GuiUseCase:
    def __init__(self) -> None:
        pass

    def generate_gui(
        self,
        worksheet_name: str,
        owner_id: str | None,
        main_blocks: list[Block | None],
        blocks: list[Block | None],
        related_function_ids: list[str | None],
    ):
        """
        reference block에 해당되는 function이 실제로 없으면 이미 삭제된 function을
        참조하는 reference block이 껴있는거임.
        순서:
        일단 워크시트를 도메인으로 만듦. 그리고 해당 도메인과 function을 스크립트로 변환함.
        변환한 스크립트를 패키징 서버로 보냄.
        넘어온 link를 db에 저장한다음 (만약 기존의 워크시트에 해당되는 link가 존재하면 그거 삭제하고 새로 덮어씌움)
        단 로그인 안했으면 넘어온 link 저장안함.
        link를 반환함.
        """
        pass
