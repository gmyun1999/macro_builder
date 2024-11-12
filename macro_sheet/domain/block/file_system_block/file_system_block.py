import re
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

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
    FIELD_TARGET = "target"
    FIELD_ACTION = "action"
    FIELD_LOC = "loc"
    FIELD_CONDITION = "condition"
    FIELD_DESTINATION = "destination"
    FIELD_RENAME = "rename"

    target: FileSystemType
    action: FileSystemAction
    loc: str
    condition: list[dict[FileConditionDetail, str] | None]
    destination: str | None
    rename: str | None
    block_type: BlockType = field(init=False)

    def __post_init__(self):
        self.block_type = BlockType.FILE_SYSTEM_BLOCK

    def to_dict(self) -> dict[str, Any]:
        base_dict = super().to_dict()
        serialized_conditions = [
            {condition_detail.value: value} if condition is not None else None
            for condition in self.condition
            for condition_detail, value in (condition.items() if condition else [])
        ]
        base_dict.update(
            {
                self.FIELD_TARGET: self.target.value,
                self.FIELD_ACTION: self.action.value,
                self.FIELD_LOC: self.loc,
                self.FIELD_CONDITION: serialized_conditions,
                self.FIELD_DESTINATION: self.destination,
                self.FIELD_RENAME: self.rename,
            }
        )
        return base_dict

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "FileSystemBlock":
        raw_conditions = data.get(cls.FIELD_CONDITION, [])
        conditions: list[dict[FileConditionDetail, str] | None] = []
        for cond in raw_conditions:
            if cond is None:
                conditions.append(None)
            else:
                condition_dict: dict[FileConditionDetail, str] = {}
                for key, value in cond.items():
                    try:
                        condition_detail = FileConditionDetail(key)
                        condition_dict[condition_detail] = value
                    except ValueError:
                        raise ValueError(f"Unrecognized FileConditionDetail: {key}")
                conditions.append(condition_dict)

        return cls(
            target=FileSystemType(data[cls.FIELD_TARGET]),
            action=FileSystemAction(data[cls.FIELD_ACTION]),
            loc=data[cls.FIELD_LOC],
            condition=conditions,
            destination=data.get(cls.FIELD_DESTINATION),
            rename=data.get(cls.FIELD_RENAME),
        )

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
