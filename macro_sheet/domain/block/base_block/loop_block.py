from dataclasses import KW_ONLY, dataclass, field
from typing import Any

from macro_sheet.domain.block.block import Block, BlockType
from macro_sheet.domain.registry import register_block_type


@register_block_type(BlockType.BASE_LOOP_BLOCK)
@dataclass(kw_only=True)
class LoopBlock(Block):
    """
    LoopBlock은 base loop block이다. 단순히 몇번 반복할지만 정의한다.
    block_type은 자식 클래스에서 오버라이드 해서 사용한다.
    """

    FIELD_ITER_CNT = "iter_cnt"
    FIELD_BODY = "body"

    iter_cnt: str  # 반복횟수
    body: list[Block] = field(default_factory=list)
    block_type: BlockType = field(init=False)

    def __post_init__(self):
        self.block_type = BlockType.BASE_LOOP_BLOCK

    def to_dict(self) -> dict[str, Any]:
        base_dict = super().to_dict()
        base_dict.update(
            {
                self.FIELD_ITER_CNT: self.iter_cnt,
                self.FIELD_BODY: [block.to_dict() for block in self.body],
            }
        )
        return base_dict

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "LoopBlock":
        return cls(
            iter_cnt=data[cls.FIELD_ITER_CNT],
            body=[
                Block.from_dict(block_data)
                for block_data in data.get(cls.FIELD_BODY, [])
            ],
        )
