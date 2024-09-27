from dataclasses import dataclass, field
from enum import StrEnum

from macro_sheet.domain.block.block import Block, BlockType
from macro_sheet.domain.registry import register_block_type


class TargetType(StrEnum):
    FILE = "FILE"
    FOLDER = "FOLDER"
    MOUSE = "MOUSE"
    API = "API"


@register_block_type(BlockType.BASE_ACTION_BLOCK)
@dataclass
class ActionBlock(Block):
    """
    ACTION 블록은 TARGET과 CONTEXT에 따라서 필요한 속성이 달라진다.
    모든 Action 블록의 공통속성을 정의한다.
    block_type은 자식 클래스에서 오버라이드 해서 사용한다.
    """

    def __post_init__(self):
        super().__post_init__()
        self.block_type = BlockType.BASE_ACTION_BLOCK


# action block dict예시:  but actionBlock 인스턴스를 직접 생성할 일은 거의 없음. ActionBlock를 상속해서 사용
#      {
#          "id": "asdasdasd"
#          "block_type" : "BASE_ACTION_BLOCK"
#      }
