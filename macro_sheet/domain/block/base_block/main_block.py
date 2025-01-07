from dataclasses import dataclass, field
from typing import Any

from macro_sheet.domain.block.block import Block, BlockType
from macro_sheet.domain.registry import register_block_type


@register_block_type(BlockType.MAIN_BLOCK)
@dataclass
class MainBlock(Block):
    FIELD_BODY = "body"

    body: list[Block] = field(default_factory=list)
    block_type: BlockType = field(init=False)

    def __post_init__(self):
        self.block_type = BlockType.MAIN_BLOCK

    def to_dict(self) -> dict[str, Any]:
        base_dict = super().to_dict()
        base_dict.update(
            {
                self.FIELD_BODY: [
                    block.to_dict() if block is not None else None
                    for block in self.body
                ]
            }
        )
        return base_dict

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MainBlock":
        if data.get(cls.FIELD_BLOCK_TYPE) != BlockType.MAIN_BLOCK.value:
            print(data.get(cls.FIELD_BLOCK_TYPE))
            print(BlockType.MAIN_BLOCK.value)
            raise ValueError(
                f"Invalid block_type for MainBlock: {data.get(cls.FIELD_BLOCK_TYPE)}"
            )

        body_data = data.get(cls.FIELD_BODY, [])
        body = [Block.from_dict(block_data) for block_data in body_data]

        return cls(body=body)
