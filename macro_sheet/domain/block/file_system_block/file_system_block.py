import re
from dataclasses import dataclass
from enum import StrEnum

from macro_sheet.domain.block.block import Block, BlockType
from macro_sheet.domain.registry import register_block_type


class FileSystemType(StrEnum):
    FILE = "FILE"
    FOLDER = "FOLDER"


class FileSystemAction(StrEnum):
    MOVE = "MOVE"
    DELETE = "DELETE"
    COPY = "COPY"
    COMPRESS = "COMPRESS"
    PRINT = "PRINT"
    RENAME = "RENAME"


class FileConditionDetail(StrEnum):
    NAME_STARTSWITH = "FILE_NAME_STARTSWITH"
    NAME_ENDSWITH = "FILE_NAME_ENDSWITH"
    NAME = "NAME"
    FILE_EXTENSION = "FILE_EXTENSION"
    FILE_SIZE_GT = "FILE_SIZE_GT"
    FILE_SIZE_LT = "FILE_SIZE_LT"
    FOLDER_SIZE_GT = "FOLDER_SIZE_GT"
    FOLDER_SIZE_LT = "FOLDER_SIZE_LT"
    FILE_CREATION_TIME_GT = "FILE_CREATION_TIME_GT"
    FILE_CREATION_TIME_LT = "FILE_CREATION_TIME_LT"
    FOLDER_CREATION_TIME_GT = "FOLDER_CREATION_TIME_GT"
    FOLDER_CREATION_TIME_LT = "FOLDER_CREATION_TIME_LT"


@register_block_type(BlockType.FILE_SYSTEM_BLOCK)
@dataclass(kw_only=True)
class FileSystemBlock(Block):
    target: FileSystemType
    action: FileSystemAction
    loc: str
    condition: list[dict[FileConditionDetail, str] | None]
    destination: str | None
    rename: str | None

    def __post_init__(self):
        super().__post_init__()
        self.block_type = BlockType.FILE_SYSTEM_BLOCK

    def validate(self) -> bool:
        safe_path_pattern = re.compile(r"^[\w\s\-\\:]+$")

        # Validate and sanitize 'loc'
        if self.loc:
            # Convert single '\' to '\\'
            if "\\" in self.loc and "\\" not in self.loc.replace("\\\\", ""):
                self.loc = self.loc.replace("\\", "\\\\")
            # Check for malicious characters
            if not safe_path_pattern.match(self.loc):
                raise ValueError(
                    "The 'loc' path contains potentially unsafe characters."
                )

        # Validate and sanitize 'destination'
        if self.destination:
            # Convert single '\' to '\\'
            if "\\" in self.destination and "\\" not in self.destination.replace(
                "\\\\", ""
            ):
                self.destination = self.destination.replace("\\", "\\\\")
            # Check for malicious characters
            if not safe_path_pattern.match(self.destination):
                raise ValueError(
                    "The 'destination' path contains potentially unsafe characters."
                )

        # Validate conditions
        for condition in self.condition:
            if not condition:
                continue

            for cond_key, cond_value in condition.items():
                # Size validation remains the same...

                # Target type validation
                file_only_conditions = {
                    FileConditionDetail.FILE_EXTENSION,
                    FileConditionDetail.FILE_SIZE_GT,
                    FileConditionDetail.FILE_SIZE_LT,
                    FileConditionDetail.FILE_CREATION_TIME_GT,
                    FileConditionDetail.FILE_CREATION_TIME_LT,
                }
                folder_only_conditions = {
                    FileConditionDetail.FOLDER_SIZE_GT,
                    FileConditionDetail.FOLDER_SIZE_LT,
                    FileConditionDetail.FOLDER_CREATION_TIME_GT,
                    FileConditionDetail.FOLDER_CREATION_TIME_LT,
                }
                # General conditions applicable to both files and folders
                general_conditions = {
                    FileConditionDetail.NAME_STARTSWITH,
                    FileConditionDetail.NAME_ENDSWITH,
                    FileConditionDetail.NAME,
                }

                if (
                    self.target == FileSystemType.FOLDER
                    and cond_key in file_only_conditions
                ):
                    raise ValueError(
                        "Target 'FOLDER' cannot have file-related conditions."
                    )
                if (
                    self.target == FileSystemType.FILE
                    and cond_key in folder_only_conditions
                ):
                    raise ValueError(
                        "Target 'FILE' cannot have folder-related conditions."
                    )

        return True
