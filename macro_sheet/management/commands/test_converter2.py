from django.core.management.base import BaseCommand

from macro_sheet.domain.block.base_block.loop_block import LoopBlock
from macro_sheet.domain.block.base_block.main_block import MainBlock
from macro_sheet.domain.block.base_block.reference_block import ReferenceBlock
from macro_sheet.domain.block.file_system_block.file_system_block import (
    FileConditionDetail,
    FileSystemAction,
    FileSystemBlock,
    FileSystemType,
)
from macro_sheet.domain.worksheet.worksheet import Worksheet


class Command(BaseCommand):
    help = "Test DomainConverter for Worksheets and Blocks"

    def handle(self, *args, **kwargs):
        worksheet = Worksheet(
            id="ws_single_block",
            name="Single Block Worksheet",
            owner_id="owner1",
            main_block=MainBlock(
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
                            LoopBlock(
                                iter_cnt="3",
                                body=[
                                    # Reference to nested_function_1 containing its own nested loop
                                    ReferenceBlock(
                                        reference_id="func_nested_2",
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
            ),
            blocks=[],
        )
        dicted = worksheet.to_dict()
        print(dicted)
