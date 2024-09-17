from dataclasses import dataclass, field
from enum import StrEnum

from macro_sheet.domain.block.block import Block, BlockType
from macro_sheet.domain.block.condition_block import ConditionBlock


class ControlType(StrEnum):
    WHILE = "while"
    IF = "if"


@dataclass
class ControlBlock(Block):
    control_type: ControlType
    conditions: list[ConditionBlock]
    body: list[Block] = field(default_factory=list)

    def __post_init__(self):
        self.block_type = BlockType.CONTROL


# control block 예시
#         {
#             "control_type": "while",
#             "condition": {
#                 "type": "file_size_gt",
#                 "value": 1024
#             },
#             "body": []
#         }
