from django.core.management.base import BaseCommand

from macro_sheet.domain.block.base_block.loop_block import LoopBlock
from macro_sheet.domain.block.base_block.main_block import MainBlock
from macro_sheet.domain.block.base_block.reference_block import ReferenceBlock
from macro_sheet.domain.block.block import BlockType
from macro_sheet.domain.block.file_system_block.file_system_block import (
    FileConditionDetail,
    FileSystemAction,
    FileSystemBlock,
    FileSystemType,
)
from macro_sheet.domain.Function.block_function import BlockFunction
from macro_sheet.domain.worksheet.worksheet import Worksheet
from macro_sheet.service.service.block_service import BlockService
from macro_sheet.service.service.command_gui_service import CommandGuiService


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        gui_service = CommandGuiService()
        block_service = BlockService()

        # 테스트 케이스 구현

        # Define BlockFunctions
        nested_function_1 = BlockFunction(
            id="func_nested_1",
            owner_id="user1",
            name="NestedFunction1",
            blocks=[
                LoopBlock(
                    iter_cnt="2",
                    body=[
                        FileSystemBlock(
                            target=FileSystemType.FILE,
                            action=FileSystemAction.DELETE,
                            loc=r"C:\Users\gmyun\OneDrive\바탕 화면\윤규민\test1",
                            condition=[{FileConditionDetail.FILE_SIZE_GT: "1000"}],
                            destination=None,
                            rename=None,
                        ),
                        FileSystemBlock(
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
                    iter_cnt="2",
                    body=[
                        FileSystemBlock(
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

        main_block = MainBlock(
            body=[
                LoopBlock(
                    iter_cnt="2",
                    body=[
                        # First FileSystemBlock in the outer loop
                        FileSystemBlock(
                            target=FileSystemType.FILE,
                            action=FileSystemAction.COPY,
                            loc="/C/user/documents/",
                            condition=[{FileConditionDetail.FILE_EXTENSION: "txt"}],
                            destination="/C/user/backup",
                            rename=None,
                        ),
                        # Nested LoopBlock inside the main LoopBlock
                        LoopBlock(
                            iter_cnt="3",
                            body=[
                                # Reference to nested_function_1 containing its own nested loop
                                ReferenceBlock(
                                    reference_id="func_nested_1",
                                ),
                                # Another FileSystemBlock in this inner loop
                                FileSystemBlock(
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
                            reference_id="func_nested_2",
                        ),
                    ],
                )
            ]
        )
        # Prepare the Worksheet with complex blocks
        worksheet = Worksheet(
            id="ws1",
            name="TestWorksheet",
            owner_id="user1",
            main_block=main_block,
            blocks=[],
        )

        main_block1 = MainBlock(
            body=[
                FileSystemBlock(
                    target=FileSystemType.FILE,
                    action=FileSystemAction.DELETE,
                    loc="C:\\Users\\gmyun\\OneDrive\\바탕 화면\\윤규민\\test1",
                    condition=[{FileConditionDetail.FILE_EXTENSION: "txt"}],
                    destination=None,
                    rename=None,
                )
            ]
        )
        worksheet1 = Worksheet(
            id="ws1", name="TestWorksheet", owner_id="user1", main_block=main_block1
        )

        script_code = block_service.generate_script_from_worksheet(
            block_functions=block_functions, worksheet=worksheet1
        )

        # 2. 생성된 파일을 패키징 서버로 전송
        download_link = (
            gui_service.get_packaged_gui_download_link_from_packaging_server(
                script_code
            )
        )

        # 3. 응답 출력
        if download_link:
            self.stdout.write(
                self.style.SUCCESS(
                    f"File uploaded successfully. Download link: {download_link}"
                )
            )
        else:
            self.stdout.write(self.style.ERROR("Failed to upload file."))
