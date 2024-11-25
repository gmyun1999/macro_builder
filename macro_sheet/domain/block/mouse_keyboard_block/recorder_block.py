from dataclasses import dataclass, field
from typing import Any

from macro_sheet.domain.block.block import Block, BlockType
from macro_sheet.domain.registry import register_block_type


@register_block_type(BlockType.RECORDER_BLOCK)
@dataclass(kw_only=True)
class RecorderBlock(Block):
    FIELD_BODY = "body"
    FIELD_BLOCK_TYPE = "block_type"

    body: dict = field(default_factory=dict)
    block_type: BlockType = field(init=False)

    def __post_init__(self):
        self.block_type = BlockType.FILE_SYSTEM_BLOCK

    def to_dict(self) -> dict[str, Any]:
        base_dict = super().to_dict()
        base_dict.update(
            {self.FIELD_BLOCK_TYPE: self.block_type.value, self.FIELD_BODY: self.body}
        )
        return base_dict

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "RecorderBlock":
        return cls(body=data[cls.FIELD_BODY])
