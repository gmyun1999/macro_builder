from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from macro_sheet.domain.block.block import Block, BlockType
from macro_sheet.domain.registry import register_block_type


class LawConditionDetail(StrEnum):
    KEYWORD = "KEYWORD"  # 검색어
    EFFECTIVE_DATE = "EFFECTIVE_DATE"  # 시행일자 범위
    MINISTRY = "MINISTRY"  # 소관부처


class LawDataType(StrEnum):
    CSV = "CSV"


@register_block_type(BlockType.LAW_API_BLOCK)
@dataclass(kw_only=True)
class LawApiBlock(Block):
    FIELD_CONDITION = "condition"
    FIELD_SAVE_DATA_TYPE = "save_data_type"
    FIELD_LOC = "loc"

    save_data_type: LawDataType
    condition: list[dict[LawConditionDetail, str] | None]
    loc: str
    block_type: BlockType = field(init=False)

    def __post_init__(self):
        self.block_type = BlockType.LAW_API_BLOCK

    def to_dict(self) -> dict[str, Any]:
        base_dict = super().to_dict()
        serialized_conditions = [
            {condition_detail.value: value} if condition is not None else None
            for condition in self.condition
            for condition_detail, value in (condition.items() if condition else [])
        ]
        base_dict.update(
            {
                self.FIELD_SAVE_DATA_TYPE: self.save_data_type,
                self.FIELD_LOC: self.loc,
                self.FIELD_CONDITION: serialized_conditions,
            }
        )
        return base_dict

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "LawApiBlock":
        raw_conditions = data.get(cls.FIELD_CONDITION, [])
        conditions: list[dict[LawConditionDetail, str] | None] = []
        for cond in raw_conditions:
            if cond is None:
                conditions.append(None)
            else:
                condition_dict: dict[LawConditionDetail, str] = {}
                for key, value in cond.items():
                    try:
                        condition_detail = LawConditionDetail(key)
                        condition_dict[condition_detail] = value
                    except ValueError:
                        raise ValueError(f"Unrecognized LawConditionDetail: {key}")
                conditions.append(condition_dict)

        return cls(
            loc=data[cls.FIELD_LOC],
            condition=conditions,
            save_data_type=LawDataType(data[cls.FIELD_SAVE_DATA_TYPE]),
        )
