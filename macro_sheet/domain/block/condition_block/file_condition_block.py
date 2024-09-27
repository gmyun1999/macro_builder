from dataclasses import dataclass
from enum import StrEnum

from macro_sheet.domain.block.block import BlockType
from macro_sheet.domain.block.condition_block.condition_block import (
    ConditionBlock,
    ConditionType,
)
from macro_sheet.domain.registry import register_block_type


class FileConditionType(StrEnum):
    FILE_NAME_STARTSWITH = "file_name_startswith"  # 파일 이름 시작
    FILE_NAME_ENDSWITH = "file_name_endswith"  # 파일 이름 끝
    FILE_CONTAINS = "file_contains"  # 파일 포함
    FILE_EXTENSION = "file_extension"  # 파일 확장자
    FILE_SIZE_GT = "file_size_gt"  # 파일 사이즈 greater then
    FILE_CREATION_TIME_LT = "file_creation_time_lt"  # 파일 생성일 less then
    FILE_MODIFICATION_TIME_GT = "file_modification_time_gt"  # 파일 수정 시간 greater then
    FILE_OWNER = "file_owner"  # 파일 소유자
    FILE_PERMISSIONS = "file_permissions"  # 파일 권한


@register_block_type(BlockType.FILE_CONDITION_BLOCK)
@dataclass
class FileConditionBlock(ConditionBlock):
    condition_type: ConditionType
    detail_condition_type: list[FileConditionType]
    value: str = ""

    def __post_init__(self):
        super().__post_init__()
        self.block_type = BlockType.FILE_CONDITION_BLOCK


# 샘플예시
#      {
#          "id": "asdasdasd"
#          "block_type" : "BASE_CONDITION_BLOCK",
#          "condition_type": "FILE",
#          "detail_condition_type": "file_extension",
#          "value": ".txt"
#      }
