from dataclasses import dataclass, field
from enum import StrEnum
from typing import ClassVar

from common.domain import Domain


class BlockType(StrEnum):
    BASE_BLOCK = "BASE_BLOCK"

    BASE_CONTROL_BLOCK = "BASE_CONTROL_BLOCK"
    BASE_CONDITION_BLOCK = "BASE_CONDITION_BLOCK"

    # base 를 상속한 block type
    FILE_SYSTEM_BLOCK = "FILE_SYSTEM_BLOCK"


@dataclass
class Block(Domain):
    block_type: BlockType

    def __post_init__(self):
        self.block_type = BlockType.BASE_BLOCK
