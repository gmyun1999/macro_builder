from dataclasses import dataclass
from enum import StrEnum

from macro_sheet.domain.block.action_block import ActionBlock, TargetType


class FileActionType(StrEnum):
    COPY = "copy"
    MOVE = "move"
    DELETE = "delete"
    REPLACE = "replace"
    ARCHIVE = "archive"
    EXTRACT = "extract"
    UPLOAD = "upload"
    DOWNLOAD = "download"
    CHMOD = "chmod"


class FileTargetDetail(StrEnum):
    FILE_NAME = "file_name"  # 파일 이름만 작업
    FILE_CONTENT = "file_content"  # 파일 내용만 작업
    FILE_METADATA = "file_metadata"  # 파일의 메타데이터 작업
    FILE = "file"  # 파일 전체 작업 (이름, 내용 포함)
    FILE_EXTENSION = "file_extension"  # 파일 확장자 작업
    FILE_SIZE = "file_size"  # 파일 크기 작업
    FILE_OWNER = "file_owner"  # 파일 소유자 작업
    FILE_PERMISSIONS = "file_permissions"  # 파일 권한 작업
    FILE_CREATION_DATE = "file_creation_date"  # 파일 생성 시간 작업
    FILE_MODIFICATION_DATE = "file_modification_date"  # 파일 수정 시간 작업
    FILE_ACCESS_DATE = "file_access_date"  # 파일 접근 시간 작업


@dataclass
class FileActionBlock(ActionBlock):
    action: FileActionType
    target_loc: str
    target_detail: FileTargetDetail
    replace_text: str | None
    chmod_value: int | None
    destination: str | None

    def __post_init__(self):
        super().__post_init__()
        self.target = TargetType.FILE


# 특정 "condition"에 "target_loc" 에 있는 target의 "target_detail"을 "destination"로 "action" 한다.
