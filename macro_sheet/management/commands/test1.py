import traceback

from django.core.management.base import BaseCommand

from macro_sheet.domain.block.block import BlockType
from macro_sheet.domain.block.file_system_block.file_system_block import (
    FileConditionDetail,
    FileSystemAction,
    FileSystemBlock,
    FileSystemType,
)
from macro_sheet.infra.code_genenerator.gui_code_generator import (
    GuiCodeGeneratorFromBlock,
)
from macro_sheet.service.i_code_generator.i_block_code_generator import (
    IGuiCodeGeneratorFromBlock,
)


class Command(BaseCommand):
    help = "Benchmark FileSystemBlock to PyQt GUI code generation performance"

    def handle(self, *args, **kwargs):
        # 테스트 케이스 정의 (기대하는 GUI 코드 포함)
        test_cases = [
            # 케이스 1: 파일 복사
            {
                "block": FileSystemBlock(
                    block_type=BlockType.FILE_SYSTEM_BLOCK,
                    target=FileSystemType.FILE,
                    action=FileSystemAction.COPY,
                    loc="/C/user/documents/",
                    condition=[{FileConditionDetail.FILE_EXTENSION: "pdf"}],
                    destination="/C/user/backup",
                    rename=None,
                ),
                "expected_code": (
                    "Get-ChildItem -Path '/C/user/documents/' | "
                    "Where-Object { $_.Extension -eq 'pdf' } | "
                    "Copy-Item -Destination '/C/user/backup'"
                ),
            },
            # 케이스 2: 파일 이동
            {
                "block": FileSystemBlock(
                    block_type=BlockType.FILE_SYSTEM_BLOCK,
                    target=FileSystemType.FILE,
                    action=FileSystemAction.MOVE,
                    loc="/C/user/photos/",
                    condition=[{FileConditionDetail.NAME_ENDSWITH: "vacation"}],
                    destination="/C/user/archive",
                    rename=None,
                ),
                "expected_code": (
                    "Get-ChildItem -Path '/C/user/photos/' | "
                    "Where-Object { $_.Name -like '*vacation' } | "
                    "Move-Item -Destination '/C/user/archive'"
                ),
            },
            # 케이스 3: 이름 변경
            {
                "block": FileSystemBlock(
                    block_type=BlockType.FILE_SYSTEM_BLOCK,
                    target=FileSystemType.FILE,
                    action=FileSystemAction.RENAME,
                    loc="/C/user/homework/",
                    condition=[{FileConditionDetail.FILE_EXTENSION: "docx"}],
                    destination=None,
                    rename="completed_homework",
                ),
                "expected_code": (
                    "$counter = 1; Get-ChildItem -Path '/C/user/homework/' | "
                    "Where-Object { $_.Extension -eq 'docx' } | "
                    "ForEach-Object { Rename-Item -Path $_.FullName -NewName ('completed_homework' + $counter + $_.Extension); $counter++ }"
                ),
            },
            # 케이스 4: 파일 삭제
            {
                "block": FileSystemBlock(
                    block_type=BlockType.FILE_SYSTEM_BLOCK,
                    target=FileSystemType.FILE,
                    action=FileSystemAction.DELETE,
                    loc="/C/user/temp/",
                    condition=[{FileConditionDetail.FILE_SIZE_LT: "500"}],
                    destination=None,
                    rename=None,
                ),
                "expected_code": (
                    "Get-ChildItem -Path '/C/user/temp/' | "
                    "Where-Object { $_.Length -lt 500 } | "
                    "Remove-Item -Recurse"
                ),
            },
        ]

        # 코드 생성기 인스턴스 생성
        generator: IGuiCodeGeneratorFromBlock = GuiCodeGeneratorFromBlock(
            template_dir="templates"
        )

        # 테스트 실행
        for i, test_case in enumerate(test_cases, start=1):
            block = test_case["block"]
            expected_code = test_case["expected_code"]

            try:
                # GUI 코드 생성
                generated_code = generator.generate_gui_code(block)

                # 기대하는 GUI 코드와 생성된 GUI 코드 비교
                if expected_code in generated_code:
                    print(f"Test Case {i}: 성공 - 기대하는 코드가 생성되었습니다.")
                else:
                    print(f"Test Case {i}: 실패 - 기대하는 코드와 생성된 코드가 일치하지 않습니다.")
                    print("Expected Code:")
                    print(expected_code)
                    print("Generated Code:")
                    print(generated_code)

            except Exception as e:
                print(f"Test Case {i}에서 GUI 코드 생성 오류: {e}")
                traceback.print_exc()
