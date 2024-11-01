from django.core.management.base import BaseCommand

from macro_sheet.domain.block.block import BlockType
from macro_sheet.domain.block.file_system_block.file_system_block import (
    FileConditionDetail,
    FileSystemAction,
    FileSystemBlock,
    FileSystemType,
)
from macro_sheet.domain.block.loop_block.loop_block import LoopBlock
from macro_sheet.domain.block.reference_block import ReferenceBlock
from macro_sheet.domain.Function.block_function import BlockFunction
from macro_sheet.domain.worksheet.worksheet import Worksheet
from macro_sheet.service.block_service import BlockService
from macro_sheet.service.gui_service import GuiService


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        gui_service = GuiService()
        block_service = BlockService()

        # 테스트 케이스 구현

        # Define BlockFunctions
        nested_function_1 = BlockFunction(
            id="func_nested_1",
            owner_id="user1",
            name="NestedFunction1",
            blocks=[
                LoopBlock(
                    block_type=BlockType.BASE_LOOP_BLOCK,
                    iter_cnt="2",
                    body=[
                        FileSystemBlock(
                            block_type=BlockType.FILE_SYSTEM_BLOCK,
                            target=FileSystemType.FILE,
                            action=FileSystemAction.DELETE,
                            loc="/C/user/temp/",
                            condition=[{FileConditionDetail.FILE_SIZE_GT: "1000"}],
                            destination=None,
                            rename=None,
                        ),
                        FileSystemBlock(
                            block_type=BlockType.FILE_SYSTEM_BLOCK,
                            target=FileSystemType.FILE,
                            action=FileSystemAction.PRINT,
                            loc="/C/user/images/",
                            condition=[{FileConditionDetail.FILE_EXTENSION: "jpg"}],
                            destination="/C/user/image_list",
                            rename=None,
                        ),
                    ],
                )
            ],
        )

        nested_function_2 = BlockFunction(
            id="func_nested_2",
            owner_id="user1",
            name="NestedFunction2",
            blocks=[
                FileSystemBlock(
                    block_type=BlockType.FILE_SYSTEM_BLOCK,
                    target=FileSystemType.FILE,
                    action=FileSystemAction.COMPRESS,
                    loc="/C/user/logs/",
                    condition=[{FileConditionDetail.FILE_EXTENSION: "log"}],
                    destination="/C/user/compressed_logs/logs.zip",
                    rename=None,
                )
            ],
        )

        nested_function_3 = BlockFunction(
            id="func_nested_3",
            owner_id="user1",
            name="NestedFunction3",
            blocks=[
                LoopBlock(
                    block_type=BlockType.BASE_LOOP_BLOCK,
                    iter_cnt="2",
                    body=[
                        FileSystemBlock(
                            block_type=BlockType.FILE_SYSTEM_BLOCK,
                            target=FileSystemType.FILE,
                            action=FileSystemAction.DELETE,
                            loc="/C/user/temp/",
                            condition=[{FileConditionDetail.FILE_SIZE_GT: "500"}],
                            destination=None,
                            rename=None,
                        )
                    ],
                )
            ],
        )

        block_functions = [nested_function_1, nested_function_2, nested_function_3]

        # Prepare the Worksheet with complex blocks
        worksheet = Worksheet(
            worksheet_id="ws1",
            name="TestWorksheet",
            owner_id="user1",
            blocks=[
                LoopBlock(
                    block_type=BlockType.BASE_LOOP_BLOCK,
                    iter_cnt="2",
                    body=[
                        # First FileSystemBlock in the outer loop
                        FileSystemBlock(
                            block_type=BlockType.FILE_SYSTEM_BLOCK,
                            target=FileSystemType.FILE,
                            action=FileSystemAction.COPY,
                            loc="/C/user/documents/",
                            condition=[{FileConditionDetail.FILE_EXTENSION: "txt"}],
                            destination="/C/user/backup",
                            rename=None,
                        ),
                        # Nested LoopBlock inside the main LoopBlock
                        LoopBlock(
                            block_type=BlockType.BASE_LOOP_BLOCK,
                            iter_cnt="3",
                            body=[
                                # Reference to nested_function_1 containing its own nested loop
                                ReferenceBlock(
                                    block_type=BlockType.REFERENCE_BLOCK,
                                    reference_id="func_nested_1",
                                ),
                                # Another FileSystemBlock in this inner loop
                                FileSystemBlock(
                                    block_type=BlockType.FILE_SYSTEM_BLOCK,
                                    target=FileSystemType.FILE,
                                    action=FileSystemAction.MOVE,
                                    loc="/C/user/downloads/",
                                    condition=[
                                        {FileConditionDetail.NAME_ENDSWITH: "_old"}
                                    ],
                                    destination="/C/user/old_downloads/",
                                    rename=None,
                                ),
                            ],
                        ),
                        # Reference to another function at the end of the main loop
                        ReferenceBlock(
                            block_type=BlockType.REFERENCE_BLOCK,
                            reference_id="func_nested_2",
                        ),
                    ],
                )
            ],
        )

        script_code = block_service.generate_script_from_worksheet(
            block_functions=block_functions, worksheet=worksheet
        )
        script_path = block_service.convert_file_from_script(script_str=script_code)

        # 2. 생성된 파일을 패키징 서버로 전송
        download_link = gui_service.send_to_package_server(script_path)

        # 3. 응답 출력
        if download_link:
            self.stdout.write(
                self.style.SUCCESS(
                    f"File uploaded successfully. Download link: {download_link}"
                )
            )
        else:
            self.stdout.write(self.style.ERROR("Failed to upload file."))
