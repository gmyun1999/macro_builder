from dataclasses import dataclass, field
from enum import StrEnum
from typing import ClassVar

from common.domain import Domain


class BlockType(StrEnum):
    BASE_BLOCK = "BASE_BLOCK"

    BASE_LOOP_BLOCK = "BASE_LOOP_BLOCK"
    BASE_CONDITION_BLOCK = "BASE_CONDITION_BLOCK"

    # base 를 상속한 block type
    FILE_SYSTEM_BLOCK = "FILE_SYSTEM_BLOCK"
    FUNCTION_BLOCK = "FUNCTION_BLOCK"

    # 다른 block의 정보를 참조하는 block type
    REFERENCE_BLOCK = "REFERENCE_BLOCK"


@dataclass
class Block(Domain):
    block_type: BlockType

    def __post_init__(self):
        self.block_type = BlockType.BASE_BLOCK

    def execute(self, *args, **kwargs):
        raise NotImplementedError("Execute method must be overridden in subclasses")
