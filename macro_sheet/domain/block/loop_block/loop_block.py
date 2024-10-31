from dataclasses import dataclass, field

from macro_sheet.domain.block.block import Block, BlockType
from macro_sheet.domain.registry import register_block_type


@register_block_type(BlockType.BASE_LOOP_BLOCK)
@dataclass
class LoopBlock(Block):
    """
    LoopBlock은 base loop block이다. 단순히 몇번 반복할지만 정의한다.
    block_type은 자식 클래스에서 오버라이드 해서 사용한다.
    """

    iter_cnt: str  # 반복횟수
    body: list[Block] = field(default_factory=list)

    def __post_init__(self):
        super().__post_init__()
        self.block_type = BlockType.BASE_LOOP_BLOCK
