from dataclasses import dataclass

from macro_sheet.domain.block.block import Block, BlockType
from macro_sheet.domain.Function.block_function import BlockFunction
from macro_sheet.domain.registry import register_block_type


@register_block_type(BlockType.REFERENCE_BLOCK)
@dataclass
class ReferenceBlock(Block):
    reference_id: str

    def __post_init__(self):
        self.block_type = BlockType.REFERENCE_BLOCK
