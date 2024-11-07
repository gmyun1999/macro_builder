from dataclasses import dataclass, field
from typing import Any

from common.domain import Domain
from macro_sheet.domain.block.base_block.main_block import MainBlock
from macro_sheet.domain.block.block import Block


@dataclass
class Worksheet(Domain):
    FIELD_ID = "id"
    FIELD_NAME = "name"
    FIELD_OWNER_ID = "owner_id"
    FIELD_MAIN_BLOCK = "main_block"
    FIELD_BLOCKS = "blocks"

    id: str
    name: str
    owner_id: str | None
    main_block: MainBlock | None
    blocks: list[Block | None] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            self.FIELD_ID: self.id,
            self.FIELD_NAME: self.name,
            self.FIELD_OWNER_ID: self.owner_id,
            self.FIELD_MAIN_BLOCK: self.main_block.to_dict()
            if self.main_block
            else None,
            self.FIELD_BLOCKS: [
                block.to_dict() if block else None for block in self.blocks
            ],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Worksheet":
        main_block_data = data.get(cls.FIELD_MAIN_BLOCK)
        main_block = MainBlock.from_dict(main_block_data) if main_block_data else None

        blocks_data = data.get(cls.FIELD_BLOCKS, [])
        blocks = [
            Block.from_dict(block_data) if block_data is not None else None
            for block_data in blocks_data
        ]

        return cls(
            id=data[cls.FIELD_ID],
            name=data[cls.FIELD_NAME],
            owner_id=data.get(cls.FIELD_OWNER_ID),
            main_block=main_block,
            blocks=blocks,
        )
