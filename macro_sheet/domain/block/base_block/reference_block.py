from dataclasses import dataclass, field
from typing import Any

from macro_sheet.domain.block.block import Block, BlockType
from macro_sheet.domain.registry import register_block_type


@register_block_type(BlockType.REFERENCE_BLOCK)
@dataclass(kw_only=True)
class ReferenceBlock(Block):
    FIELD_REFERENCE_ID = "reference_id"
    FIELD_REFERENCE_FUNCTION_NAME = "reference_function_name"

    reference_id: str  # function의 id와 동일함.
    reference_function_name: str = "UnKnown"
    block_type: BlockType = field(init=False)

    def __post_init__(self):
        self.block_type = BlockType.REFERENCE_BLOCK

    def to_dict(self) -> dict[str, Any]:
        base_dict = super().to_dict()
        base_dict.update(
            {
                self.FIELD_REFERENCE_ID: self.reference_id,
                self.FIELD_REFERENCE_FUNCTION_NAME: self.reference_function_name,
            }
        )
        return base_dict

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ReferenceBlock":
        return cls(
            reference_id=data[cls.FIELD_REFERENCE_ID],
            reference_function_name=data.get(
                cls.FIELD_REFERENCE_FUNCTION_NAME, "UnKnown"
            ),
            position=data.get(cls.FIELD_POSITION),
        )
