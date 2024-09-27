from dataclasses import dataclass
from enum import StrEnum

from macro_sheet.domain.block.block import Block, BlockType
from macro_sheet.domain.registry import register_block_type


class ConditionType(StrEnum):
    FILE = "FILE"
    API = "API"
    MOUSE = "MOUSE"
    KEYBOARD = "KEYBOARD"


@register_block_type(BlockType.BASE_CONDITION_BLOCK)
@dataclass
class ConditionBlock(Block):
    """
    conditionBlock의 공통적인 속성을 정의한다.
    """

    def __post_init__(self):
        super().__post_init__()
        self.block_type = BlockType.BASE_CONDITION_BLOCK


# condition block 문법: {"condition_type" 의 "detail_condition_type"가 value 인경우}
# condition block dict예시:  but conditionBlock 인스턴스를 직접 생성할 일은 거의 없음.
#      {
#          "id": "asdasdasd"
#          "block_type" : "BASE_CONDITION_BLOCK"
#      }
