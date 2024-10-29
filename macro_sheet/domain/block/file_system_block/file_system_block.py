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
@dataclass
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
        # Action에 따른 기본 검증
        if (
            self.action
            in {
                FileSystemAction.MOVE,
                FileSystemAction.COPY,
                FileSystemAction.COMPRESS,
                FileSystemAction.PRINT,
            }
            and not self.destination
        ):
            raise ValueError(f"Action '{self.action}' requires a destination path.")
        if self.action == FileSystemAction.RENAME and not self.rename:
            raise ValueError(
                "Action 'RENAME' requires a new name in the 'rename' attribute."
            )

        # target 유형에 따라 condition을 단일 반복문으로 검증
        for condition in self.condition:
            if not condition:
                continue

            for cond_key, cond_value in condition.items():
                # FILE_SIZE_GT와 FILE_SIZE_LT 검증
                if cond_key in {
                    FileConditionDetail.FILE_SIZE_GT,
                    FileConditionDetail.FILE_SIZE_LT,
                }:
                    size = int(cond_value)
                    if size < 1:
                        raise ValueError(
                            f"{cond_key.value} condition requires a size of at least 1."
                        )

                # target 유형에 따른 condition 검증
                if self.target == FileSystemType.FOLDER and "FILE" in cond_key.value:
                    raise ValueError(
                        "Target 'FOLDER' cannot have file-related conditions."
                    )
                if self.target == FileSystemType.FILE and "FOLDER" in cond_key.value:
                    raise ValueError(
                        "Target 'FILE' cannot have folder-related conditions."
                    )

        return True

    def to_powershell(self) -> str:
        # 조건 매핑 딕셔너리 생성
        condition_map = {
            FileConditionDetail.FILE_EXTENSION: lambda value: f"$_.Extension -eq '{value}'",
            FileConditionDetail.NAME_STARTSWITH: lambda value: f"$_.Name -like '{value}*'",
            FileConditionDetail.NAME_ENDSWITH: lambda value: f"$_.Name -like '*{value}'",
            FileConditionDetail.FILE_SIZE_GT: lambda value: f"$_.Length -gt {value}",
            FileConditionDetail.FILE_SIZE_LT: lambda value: f"$_.Length -lt {value}",
            FileConditionDetail.FILE_CREATION_TIME_GT: lambda value: f"$_.CreationTime -gt [datetime]'{value}'",
            FileConditionDetail.FILE_CREATION_TIME_LT: lambda value: f"$_.CreationTime -lt [datetime]'{value}'",
        }

        # 조건 필터링 생성
        conditions = [
            condition_map[cond_key](cond_value)
            for condition in self.condition
            if condition
            for cond_key, cond_value in condition.items()
            if cond_key in condition_map
        ]

        condition_str = (
            f" | Where-Object {{ {' -and '.join(conditions)} }}" if conditions else ""
        )
        base_command = f"Get-ChildItem -Path '{self.loc}'{condition_str}"

        # Action에 따른 PowerShell 명령어 생성
        action_commands = {
            FileSystemAction.COPY: f"{base_command} | Copy-Item -Destination '{self.destination}'",
            FileSystemAction.RENAME: (
                f"$counter = 1; "
                f"{base_command} | ForEach-Object {{ "
                f"Rename-Item -Path $_.FullName -NewName ('{self.rename}' + $counter + $_.Extension); "
                f"$counter++ }}"
            ),
            FileSystemAction.PRINT: f"{base_command} | ForEach-Object {{ $_.FullName }} | Out-File -FilePath '{self.destination}\\file_list.txt' -Encoding UTF8",
            FileSystemAction.COMPRESS: f"{base_command} | Compress-Archive -DestinationPath '{self.destination}'",
            FileSystemAction.DELETE: f"{base_command} | Remove-Item -Recurse",
            FileSystemAction.MOVE: f"{base_command} | Move-Item -Destination '{self.destination}'",
        }

        return action_commands.get(self.action, "지원되지 않는 작업입니다.")
