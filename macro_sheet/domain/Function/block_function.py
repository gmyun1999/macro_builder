from dataclasses import dataclass, field
from typing import Any

from macro_sheet.domain.block.block import Block


@dataclass
class BlockFunction:
    FIELD_ID = "id"
    FIELD_OWNER_ID = "owner_id"
    FIELD_NAME = "name"
    FIELD_BLOCKS = "blocks"
    FIELD_RAW_BLOCKS = "raw_blocks"

    id: str
    owner_id: str
    name: str
    blocks: list[Block] = field(default_factory=list)
    raw_blocks: list = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            self.FIELD_ID: self.id,
            self.FIELD_OWNER_ID: self.owner_id,
            self.FIELD_NAME: self.name,
            self.FIELD_BLOCKS: [
                block.to_dict() if block is not None else None for block in self.blocks
            ],
            self.FIELD_RAW_BLOCKS: self.raw_blocks,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BlockFunction":
        blocks_data = data.get(cls.FIELD_BLOCKS, [])
        blocks = [Block.from_dict(block_data) for block_data in blocks_data]

        return cls(
            id=data[cls.FIELD_ID],
            owner_id=data[cls.FIELD_OWNER_ID],
            name=data[cls.FIELD_NAME],
            blocks=blocks,
            raw_blocks=data[cls.FIELD_RAW_BLOCKS],
        )
