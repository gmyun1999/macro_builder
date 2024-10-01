from django.core.management.base import BaseCommand

from macro_sheet.domain.block.action_block.file_action_block import FileActionBlock
from macro_sheet.domain.block.condition_block.file_condition_block import (
    FileConditionBlock,
)
from macro_sheet.domain.block.control_block.control_block import ControlBlock
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
            block_type="FILE_CONDITION_BLOCK",
            condition_type="file_size_gt",
            detail_condition_type=["FILE_SIZE"],
            value="400",
        )

        # FileActionBlock 생성
        file_action = FileActionBlock(
            id="fileaction001",
            block_type="FILE_ACTION_BLOCK",
            action="MOVE",
            target_loc="/source/path",
            target_detail="FILE_NAME",
            replace_text=None,
            chmod_value=None,
            destination="/destination/path",
            target="FILE",
        )

        # ControlBlock (WHILE) 생성
        control_block = ControlBlock(
            id="control001",
            block_type="BASE_CONTROL_BLOCK",
            control_type="WHILE",
            conditions=[file_condition],
            body=[file_action],
        )

        # 코드 생성기 인스턴스 생성
        generator: IGuiCodeGeneratorFromBlock = GuiCodeGeneratorFromBlock(
            template_dir="templates"
        )

        # GUI 코드 생성
        gui_code = generator.generate_gui_code(control_block)

        # 생성된 코드 파일로 저장
        with open("generated_gui.py", "w") as f:
            f.write(gui_code)

        print("GUI 코드가 'generated_gui.py' 파일로 생성되었습니다.")
