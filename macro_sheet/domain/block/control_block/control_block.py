from dataclasses import dataclass, field
from enum import StrEnum

from macro_sheet.domain.block.block import Block, BlockType
from macro_sheet.domain.block.condition_block.condition_block import ConditionBlock
from macro_sheet.domain.registry import register_block_type


class ControlType(StrEnum):
    WHILE = "while"
    IF = "if"


@register_block_type(BlockType.BASE_CONTROL_BLOCK)
@dataclass
class ControlBlock(Block):
    """
    ControlBlock은 TARGET과 CONTEXT에 따라서 필요한 속성이 달라질수있다.
    모든 control 블록의 공통속성을 정의한다.
    block_type은 자식 클래스에서 오버라이드 해서 사용한다.
    """

    control_type: ControlType
    conditions: list[ConditionBlock]
    body: list[Block] = field(default_factory=list)

    def __post_init__(self):
        super().__post_init__()
        self.block_type = BlockType.BASE_CONTROL_BLOCK


# control block dict예시
#         {
#             "id": "ihbqjunwddqwihjdw"
#             "block_type": "BASE_CONTROL_BLOCK",
#             "control_type": "while",
#             "condition": {
#                 "type": "file_size_gt",
#                 "value": 1024
#             },
#             "body": []
#         }
