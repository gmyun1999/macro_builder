from dataclasses import dataclass, field
from enum import StrEnum
from typing import ClassVar


class BlockType(StrEnum):
    BASE_BLOCK = "BASE_BLOCK"

    BASE_CONTROL_BLOCK = "BASE_CONTROL_BLOCK"
    BASE_CONDITION_BLOCK = "BASE_CONDITION_BLOCK"
    BASE_ACTION_BLOCK = "BASE_ACTION_BLOCK"

    # base 를 상속한 block type
    FILE_ACTION_BLOCK = "FILE_ACTION_BLOCK"
    FILE_CONTROL_BLOCK = "FILE_CONTROL_BLOCK"
    FILE_CONDITION_BLOCK = "FILE_CONDITION_BLOCK"


@dataclass
class Block:
    # FIELD_ID = "id"

    id: str
    block_type: BlockType

    def __post_init__(self):
        self.block_type = BlockType.BASE_BLOCK
