from dataclasses import dataclass
from enum import StrEnum

from macro_sheet.domain.block.action_block.action_block import ActionBlock, TargetType
from macro_sheet.domain.block.block import BlockType
from macro_sheet.domain.registry import register_block_type


class FileActionType(StrEnum):
    COPY = "COPY"
    MOVE = "MOVE"
    DELETE = "DELETE"
    REPLACE = "REPLACE"
    ARCHIVE = "ARCHIVE"
    EXTRACT = "EXTRACT"
    UPLOAD = "UPLOAD"
    DOWNLOAD = "DOWNLOAD"
    CHMOD = "CHMOD"


class FileTargetDetail(StrEnum):
    FILE_NAME = "FILE_NAME"  # 파일 이름만 작업
    FILE_CONTENT = "FILE_CONTENT"  # 파일 내용만 작업
    FILE_METADATA = "FILE_METADATA"  # 파일의 메타데이터 작업
    FILE = "FILE"  # 파일 전체 작업 (이름, 내용 포함)
    FILE_EXTENSION = "FILE_EXTENSION"  # 파일 확장자 작업
    FILE_SIZE = "FILE_SIZE"  # 파일 크기 작업
    FILE_OWNER = "FILE_OWNER"  # 파일 소유자 작업
    FILE_PERMISSIONS = "FILE_PERMISSIONS"  # 파일 권한 작업
    FILE_CREATION_DATE = "FILE_CREATION_DATE"  # 파일 생성 시간 작업
    FILE_MODIFICATION_DATE = "FILE_MODIFICATION_DATE"  # 파일 수정 시간 작업
    FILE_ACCESS_DATE = "FILE_ACCESS_DATE"  # 파일 접근 시간 작업


@register_block_type(BlockType.FILE_ACTION_BLOCK)
@dataclass
class FileActionBlock(ActionBlock):
    action: FileActionType
    target_loc: str  # ex) 파일의 위치
    target_detail: FileTargetDetail  # ex) 파일의 이름, 파일 그자체 등등
    replace_text: str | None  # ex) 파일 이름 교체와 같이
    chmod_value: int | None
    destination: str | None
    target: TargetType = TargetType.FILE

    def __post_init__(self):
        super().__post_init__()
        self.block_type = BlockType.FILE_ACTION_BLOCK


# FileActionBlock문법: "target_loc" 에 있는 target의 "target_detail"을 "destination"로 "action" 한다.
