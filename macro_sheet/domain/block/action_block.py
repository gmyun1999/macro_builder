from dataclasses import dataclass
from enum import StrEnum

from macro_sheet.domain.block.block import Block, BlockType
from macro_sheet.domain.block.file.action_block import FileTargetDetail


class TargetType(StrEnum):
    FILE = "FILE"
    FOLDER = "FOLDER"
    MOUSE = "MOUSE"


@dataclass
class ActionBlock(Block):
    target: TargetType

    def __post_init__(self):
        self.block_type = BlockType.ACTION
