from dataclasses import dataclass

from macro_sheet.domain.block.block import Block, BlockType
from macro_sheet.domain.Function.block_function import BlockFunction
from macro_sheet.domain.registry import register_block_type


@register_block_type(BlockType.REFERENCE_BLOCK)
@dataclass(kw_only=True)
class ReferenceBlock(Block):
    reference_id: str  # function의 id와 동일함.
    reference_function_name: str = "UnKnown"

    def __post_init__(self):
        self.block_type = BlockType.REFERENCE_BLOCK
