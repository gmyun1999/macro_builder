from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from macro_sheet.domain.block.block import Block, BlockType
from macro_sheet.domain.block.file.condition_block import FileConditionType


class ConditionType(StrEnum):
    FILE = "FILE"
    API = "API"
    MOUSE = "MOUSE"
    KEYBOARD = "KEYBOARD"


@dataclass
class ConditionBlock(Block):
    condition_type: ConditionType
    detail_condition_type: list[FileConditionType | Any]
    value: str = ""
    body: list[Block | None] = field(default_factory=list)

    def __post_init__(self):
        self.block_type = BlockType.CONDITION


# condition block 예시
#      {
#          "condition_type": "FILE"
#          "detail_condition_type": "file_extension",
#          "value": ".txt"
#          "body": [
#
#
#          ]
#      }
