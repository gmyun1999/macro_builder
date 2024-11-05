from dataclasses import KW_ONLY, dataclass

from macro_sheet.domain.block.block import Block, BlockType
from macro_sheet.domain.registry import register_block_type


@register_block_type(BlockType.BASE_CONDITION_BLOCK)
@dataclass(kw_only=True)
class ConditionBlock(Block):
    """
    conditionBlock의 공통적인 속성을 정의한다.
    """

    def __post_init__(self):
        super().__post_init__()
        self.block_type = BlockType.BASE_CONDITION_BLOCK
