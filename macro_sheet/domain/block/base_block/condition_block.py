from dataclasses import KW_ONLY, dataclass, field
from typing import Any

from macro_sheet.domain.block.block import Block, BlockType
from macro_sheet.domain.registry import register_block_type


@register_block_type(BlockType.BASE_CONDITION_BLOCK)
@dataclass
class ConditionBlock(Block):
    # ConditionBlock에 특화된 필드가 있다면 추가
    block_type: BlockType = field(init=False)

    def __post_init__(self):
        self.block_type = BlockType.BASE_CONDITION_BLOCK

    def to_dict(self) -> dict[str, Any]:
        base_dict = super().to_dict()
        # 추가 필드가 있다면 여기서 업데이트
        return base_dict

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ConditionBlock":
        return cls(
            position=data.get(cls.FIELD_POSITION)
            # 추가 필드가 있다면 여기서 초기화
        )
