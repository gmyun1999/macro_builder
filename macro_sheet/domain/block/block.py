from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from common.domain import Domain


class BlockType(StrEnum):
    BASE_BLOCK = "BASE_BLOCK"
    MAIN_BLOCK = "MAIN_BLOCK"  # WORKSHEET에서만 사용가능.

    BASE_LOOP_BLOCK = "BASE_LOOP_BLOCK"
    BASE_CONDITION_BLOCK = "BASE_CONDITION_BLOCK"

    # base 를 상속한 block type
    FILE_SYSTEM_BLOCK = "FILE_SYSTEM_BLOCK"
    RECORDER_BLOCK = "RECORDER_BLOCK"
    LAW_API_BLOCK = "LAW_API_BLOCK"

    # 다른 block의 정보를 참조하는 block type
    REFERENCE_BLOCK = "REFERENCE_BLOCK"


@dataclass
class Block:
    FIELD_BLOCK_TYPE = "block_type"

    block_type: BlockType

    def to_dict(self) -> dict[str, Any]:
        return {self.FIELD_BLOCK_TYPE: self.block_type.value}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Block":
        block_type = data.get(cls.FIELD_BLOCK_TYPE)
        if not block_type:
            raise ValueError("block_type is required for Block deserialization")

        from macro_sheet.domain.registry import BLOCK_TYPE_REGISTRY

        block_cls = BLOCK_TYPE_REGISTRY.get(block_type)
        if not block_cls:
            raise ValueError(f"Unrecognized block_type: {block_type}")

        return block_cls.from_dict(data)
