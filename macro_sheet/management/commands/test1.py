from django.core.management.base import BaseCommand

from macro_sheet.domain.block.action_block.action_block import TargetType
from macro_sheet.domain.block.action_block.file_action_block import (
    FileActionBlock,
    FileActionType,
    FileTargetDetail,
)
from macro_sheet.domain.block.block import BlockType
from macro_sheet.domain.block.condition_block.condition_block import ConditionType
from macro_sheet.domain.block.condition_block.file_condition_block import (
    FileConditionBlock,
    FileConditionType,
)
from macro_sheet.domain.block.control_block.control_block import (
    ControlBlock,
    ControlType,
)
from macro_sheet.infra.code_genenerator.gui_code_generator import (
    GuiCodeGeneratorFromBlock,
)
from macro_sheet.service.i_code_generator.i_block_code_generator import (
    IGuiCodeGeneratorFromBlock,
)


class Command(BaseCommand):
    help = "Benchmark GenericSerializer deserialization performance"

    def handle(self, *args, **kwargs):
        # Define all test cases
        file_condition = FileConditionBlock(
            id="filecond001",
            block_type=BlockType.FILE_CONDITION_BLOCK,
            condition_type=ConditionType.FILE,  # 대분류: 파일 관련 조건임을 명시
            detail_condition_type=[FileConditionType.FILE_SIZE_GT],  # 구체적 조건
            value="400",
        )

        # FileActionBlock 생성
        file_action = FileActionBlock(
            id="fileaction001",
            block_type=BlockType.FILE_ACTION_BLOCK,  # BlockType 열거형으로 변경
            action=FileActionType.MOVE,  # FileActionType 열거형으로 변경
            target_loc="/source/path",
            target_detail=FileTargetDetail.FILE_NAME,  # FileTargetDetail 열거형으로 변경
            replace_text=None,
            chmod_value=None,
            destination="/destination/path",
            target=TargetType.FILE,  # TargetType 열거형으로 변경
        )

        # ControlBlock (WHILE) 생성
        control_block = ControlBlock(
            id="control001",
            block_type=BlockType.BASE_CONTROL_BLOCK,  # BlockType 열거형으로 변경
            control_type=ControlType.WHILE,  # ControlType 열거형으로 변경
            conditions=[file_condition],
            body=[file_action],
        )
        # 최하위의 액션 블록 (예: 특정 파일 이동)
        deep_action_block = FileActionBlock(
            id="action_deep",
            block_type=BlockType.FILE_ACTION_BLOCK,
            action=FileActionType.MOVE,
            target_loc="/deep/source/path",
            target_detail=FileTargetDetail.FILE_NAME,
            replace_text=None,
            chmod_value=None,
            destination="/deep/destination/path",
            target=TargetType.FILE,
        )

        # 조건문이 있는 블록 (예: 파일 이름이 'data'로 시작하는지 확인)
        deep_if_block = ControlBlock(
            id="if_deep",
            block_type=BlockType.BASE_CONTROL_BLOCK,
            control_type=ControlType.IF,
            conditions=[
                FileConditionBlock(
                    id="cond_deep",
                    block_type=BlockType.FILE_CONDITION_BLOCK,
                    condition_type=ConditionType.FILE,
                    detail_condition_type=[FileConditionType.FILE_NAME_STARTSWITH],
                    value="data",
                )
            ],
            body=[deep_action_block],
        )

        # 더 상위의 while 블록
        inner_while_block = ControlBlock(
            id="while_inner",
            block_type=BlockType.BASE_CONTROL_BLOCK,
            control_type=ControlType.WHILE,
            conditions=[
                FileConditionBlock(
                    id="cond_inner",
                    block_type=BlockType.FILE_CONDITION_BLOCK,
                    condition_type=ConditionType.FILE,
                    detail_condition_type=[FileConditionType.FILE_SIZE_GT],
                    value="100",
                )
            ],
            body=[deep_if_block],
        )

        # 또 다른 상위의 while 블록
        outer_while_block = ControlBlock(
            id="while_outer",
            block_type=BlockType.BASE_CONTROL_BLOCK,
            control_type=ControlType.WHILE,
            conditions=[
                FileConditionBlock(
                    id="cond_outer",
                    block_type=BlockType.FILE_CONDITION_BLOCK,
                    condition_type=ConditionType.FILE,
                    detail_condition_type=[FileConditionType.FILE_SIZE_GT],
                    value="200",
                )
            ],
            body=[inner_while_block],
        )

        # 최상위 while 블록
        top_while_block = ControlBlock(
            id="while_top",
            block_type=BlockType.BASE_CONTROL_BLOCK,
            control_type=ControlType.WHILE,
            conditions=[
                FileConditionBlock(
                    id="cond_top",
                    block_type=BlockType.FILE_CONDITION_BLOCK,
                    condition_type=ConditionType.FILE,
                    detail_condition_type=[FileConditionType.FILE_SIZE_GT],
                    value="400",
                )
            ],
            body=[outer_while_block],
        )

        # 코드 생성기 인스턴스 생성
        generator: IGuiCodeGeneratorFromBlock = GuiCodeGeneratorFromBlock(
            template_dir="templates"
        )

        # GUI 코드 생성
        gui_code = generator.generate_gui_code(top_while_block)

        with open("generated_gui.py", "w", encoding="utf-8") as f:
            f.write(gui_code)

        print("GUI 코드가 'generated_gui.py' 파일로 생성되었습니다.")
