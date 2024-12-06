import uuid
from typing import Any

import httpx

from macro_sheet.domain.block.api_block.law_api_block import LawApiBlock
from macro_sheet.domain.block.base_block.loop_block import LoopBlock
from macro_sheet.domain.block.base_block.main_block import MainBlock
from macro_sheet.domain.block.base_block.reference_block import ReferenceBlock
from macro_sheet.domain.block.block import Block, BlockType
from macro_sheet.domain.block.file_system_block.file_system_block import (
    FileConditionDetail,
    FileSystemAction,
    FileSystemBlock,
    FileSystemType,
)
from macro_sheet.domain.block.mouse_keyboard_block.recorder_block import RecorderBlock
from macro_sheet.domain.Function.block_function import BlockFunction
from macro_sheet.domain.worksheet.worksheet import Worksheet


class BlockService:
    def __init__(self):
        self.powershell_converter = PowerShellConverter()
        self.generated_functions = {}

    def convert_file_system_block_to_str_code(
        self, block: FileSystemBlock, indent=0, encoding="utf-8"
    ) -> str:
        """
        Converts a FileSystemBlock to an executable PowerShell command string,
        wrapped in a Python subprocess command.
        """
        indent_str = " " * indent
        # Use the PowerShellConverter to generate the command
        original_powershell_command = (
            self.powershell_converter.convert_fileblock_to_powershell(block)
        )
        # Prepend 'chcp 65001;' to set the code page to UTF-8
        powershell_command = f"chcp 65001; {original_powershell_command}"

        # Create the subprocess command string with proper indentation and encoding
        subprocess_command = (
            f"{indent_str}subprocess.run(['powershell', '-Command', r\"{powershell_command}\"], "
            f"encoding='{encoding}', errors='ignore', check=True)"
        )  # noqa: E501
        return subprocess_command

    def convert_loop_block_to_str_code(
        self,
        block: LoopBlock,
        block_functions: list[BlockFunction],
        indent=0,
        visited=None,
    ) -> str:
        """
        Converts a LoopBlock to an executable Python loop with nested commands."""
        indent_str = " " * indent
        commands = []
        iter_cnt = block.iter_cnt
        commands.append(f"{indent_str}for _ in range({iter_cnt}):")

        for inner_block in block.body:
            if isinstance(inner_block, FileSystemBlock):
                cmd = self.convert_file_system_block_to_str_code(
                    inner_block, indent=indent + 4
                )
                commands.append(cmd)
            elif isinstance(inner_block, LoopBlock):
                cmd = self.convert_loop_block_to_str_code(
                    inner_block, block_functions, indent=indent + 4, visited=visited
                )
                commands.append(cmd)
            elif isinstance(inner_block, ReferenceBlock):
                cmd = self.render_reference_block_to_str_code(
                    inner_block, block_functions, indent=indent + 4, visited=visited
                )
                commands.append(cmd)
            elif isinstance(inner_block, RecorderBlock):
                cmd = self.render_recorder_block_to_str_code(
                    inner_block, indent=indent + 4
                )
                commands.append(cmd)

        return "\n".join(commands)

    def render_reference_block_to_str_code(
        self,
        reference_block: ReferenceBlock,
        block_functions: list[BlockFunction],
        indent=0,
        visited=None,
    ) -> str:
        """
        Renders a ReferenceBlock to a function call, generating the function if not already generated.
        Detects cyclic references using the 'visited' set.
        """
        indent_str = " " * indent
        reference_id = reference_block.reference_id

        if visited is None:
            visited = set()

        if reference_id in visited:
            raise ValueError(
                f"Cyclic reference detected for BlockFunction id: {reference_id}"
            )

        visited.add(reference_id)

        # Check if the function is already generated
        if reference_id not in self.generated_functions:
            # Find the referenced BlockFunction
            referenced_function = next(
                (bf for bf in block_functions if bf.id == reference_id), None
            )
            if not referenced_function:
                raise ValueError(f"No BlockFunction found with id: {reference_id}")

            func_body = []
            func_body.append(f"def {reference_id}():")

            for block in referenced_function.blocks:
                if isinstance(block, FileSystemBlock):
                    cmd = self.convert_file_system_block_to_str_code(block, indent=4)
                    func_body.append(cmd)
                elif isinstance(block, LoopBlock):
                    cmd = self.convert_loop_block_to_str_code(
                        block, block_functions, indent=4, visited=visited
                    )
                    func_body.append(cmd)
                elif isinstance(block, ReferenceBlock):
                    cmd = self.render_reference_block_to_str_code(
                        block, block_functions, indent=4, visited=visited
                    )
                    func_body.append(cmd)
                elif isinstance(block, RecorderBlock):
                    cmd = self.render_recorder_block_to_str_code(
                        block, indent=indent + 4
                    )
                    func_body.append(cmd)
            # Store the generated function code
            self.generated_functions[reference_id] = "\n".join(func_body)

        # Return the function call with proper indentation
        return f"{indent_str}{reference_id}()"

    def render_api_block_to_str_code(self, block: LawApiBlock) -> str:
        return "pass"

    def render_recorder_block_to_str_code(
        self, block: RecorderBlock, indent: int = 4
    ) -> str:
        """
        Renders a RecorderBlock to a dynamically generated Python function and
        returns the function call code.

        Function definition is stored in `self.generated_functions`.

        Args:
            block (RecorderBlock): The recorder block to convert.
            function_counter (int): Counter to ensure unique function names.
            indent (int): Number of spaces to indent the function body.
        """
        function_indent = 4
        # Generate a unique function name based on the counter
        function_name = f"send_recorder_data_{uuid.uuid4().hex}"

        # Recorder block's data (convert to dict if necessary)
        recorder_data = block.body  # Assuming RecorderBlock has a `to_dict()` method

        # Indent strings
        function_indent_str = " " * function_indent
        indent_str = " " * indent
        # Define the function code with controlled indentation
        function_body = (
            f"def {function_name}():\n"
            f'{function_indent_str}host = "127.0.0.1"\n'
            f"{function_indent_str}port = 5262\n"
            f'{function_indent_str}api_key = "test_key"\n'
            f'{function_indent_str}endpoint = "/execute_recorder/"\n'
            f'{function_indent_str}url = f"http://{{host}}:{{port}}{{endpoint}}"\n\n'
            f'{function_indent_str}headers = {{"Content-Type": "application/json", "Api-Key": api_key}}\n'
            f"{function_indent_str}recorder_data = {recorder_data}\n\n"
            f"{function_indent_str}try:\n"
            f"{function_indent_str * 2}response = requests.post(url, json=recorder_data, headers=headers)\n"
            f"{function_indent_str * 2}if response.status_code == 200:\n"
            f'{function_indent_str * 3}print("recorder 실행 성공")\n'
            f"{function_indent_str * 2}else:\n"
            f'{function_indent_str * 3}print("recorder 실행 실패")\n'
            f"{function_indent_str}except Exception as e:\n"
            f'{function_indent_str * 2}print(f"에러: {{str(e)}}")'
        )

        # Store the function definition in `self.generated_functions`
        self.generated_functions[function_name] = function_body

        # Return the function call code
        return f"{indent_str}{function_name}()"

    def generate_script_from_worksheet(
        self, main_block: MainBlock, block_functions: list[BlockFunction]
    ) -> str:
        """
        Generates the full Python script from the worksheet and block functions.
        """
        self.generated_functions = {}
        commands = []

        if not main_block.body:
            raise ValueError("main block 의 내용이 존재해야함.")

        for block in main_block.body:
            if isinstance(block, FileSystemBlock):
                cmd = self.convert_file_system_block_to_str_code(block)
                commands.append(cmd)
            elif isinstance(block, LoopBlock):
                cmd = self.convert_loop_block_to_str_code(block, block_functions)
                commands.append(cmd)
            elif isinstance(block, ReferenceBlock):
                cmd = self.render_reference_block_to_str_code(block, block_functions)
                commands.append(cmd)
            elif isinstance(block, RecorderBlock):
                # Generate the recorder function and its invocation
                cmd = self.render_recorder_block_to_str_code(block)
                commands.append(cmd)
            elif isinstance(block, LawApiBlock):
                cmd = self.render_api_block_to_str_code(block)
                commands.append(cmd)
            else:
                raise TypeError(f"Unsupported block type: {type(block).__name__}")

        # Combine all generated functions and main code
        functions_code = "\n\n".join(self.generated_functions.values())
        main_code = "\n".join(commands)

        full_script = (
            "import subprocess\nimport requests\n\n" f"{functions_code}\n\n{main_code}"
        )

        return full_script

    def find_reference_blocks_in_block(self, block: Block) -> list[dict[str, str]]:
        block_dict = block.to_dict()
        references = []
        seen_references = set()

        def traverse(block: dict[str, Any]):
            block_type = block.get(Block.FIELD_BLOCK_TYPE)
            if block_type == BlockType.REFERENCE_BLOCK.value:
                reference_id = block.get(ReferenceBlock.FIELD_REFERENCE_ID)
                reference_function_name = block.get(
                    ReferenceBlock.FIELD_REFERENCE_FUNCTION_NAME, "UnKnown"
                )
                reference_key = (reference_id, reference_function_name)
                if reference_key not in seen_references:
                    seen_references.add(reference_key)
                    references.append(
                        {
                            "reference_id": reference_id,
                            "reference_function_name": reference_function_name,
                        }
                    )

            elif "body" in block and isinstance(block["body"], list):
                for child_block in block["body"]:
                    traverse(child_block)

        traverse(block_dict)
        return references

    def convert_file_from_script(self, script_str: str):
        # Python 파일로 저장
        script_path = "generated_execute_script.py"  # 로컬 경로에 파일 저장
        with open(script_path, "w", encoding="utf-8") as script_file:
            script_file.write(script_str)

        return script_path


class PowerShellConverter:
    def convert_fileblock_to_powershell(self, block: FileSystemBlock) -> str:
        """Converts a FileSystemBlock to a PowerShell command."""
        # Generate the base command
        base_command = self._create_base_command(block)

        # Generate search conditions
        search_condition = self._create_search_condition(block)

        # Generate the action command
        action_command = self._create_action_command(block)

        # For RENAME action, include counter initialization
        if block.action == FileSystemAction.RENAME:
            if search_condition:
                return f"$counter = 1; {base_command} | Where-Object {{ {search_condition} }} | {action_command}"
            return f"$counter = 1; {base_command} | {action_command}"

        # For other actions
        if search_condition:
            return f"{base_command} | Where-Object {{ {search_condition} }} | {action_command}"
        return f"{base_command} | {action_command}"

    def _create_base_command(self, block: FileSystemBlock) -> str:
        """Creates the Get-ChildItem base command."""
        path = f"'{block.loc}'"
        if block.target == FileSystemType.FOLDER:
            return f"Get-ChildItem -Path {path} -Directory"
        return f"Get-ChildItem -Path {path} -File"

    def _create_search_condition(self, block: FileSystemBlock) -> str:
        """Generates search conditions for the PowerShell command."""
        # Determine the property to use based on the target type
        if block.target == FileSystemType.FILE:
            name_property = "$_.Name"  # 확장자를 포함한 이름
        else:  # For FOLDER target
            name_property = "$_.Name"

        condition_map = {
            FileConditionDetail.FILE_EXTENSION: lambda v: f"$_.Extension -eq '.{v}'",
            FileConditionDetail.NAME_STARTSWITH: lambda v: f"{name_property} -like '{v}*'",
            FileConditionDetail.NAME_ENDSWITH: lambda v: f"{name_property} -like '*{v}'",
            FileConditionDetail.NAME: lambda v: f"{name_property} -eq '{v}'",
            FileConditionDetail.FILE_SIZE_GT: lambda v: f"$_.Length -gt {v}",
            FileConditionDetail.FILE_SIZE_LT: lambda v: f"$_.Length -lt {v}",
            FileConditionDetail.FILE_CREATION_TIME_GT: lambda v: f"$_.CreationTime -gt [datetime]'{v}'",
            FileConditionDetail.FILE_CREATION_TIME_LT: lambda v: f"$_.CreationTime -lt [datetime]'{v}'",
            FileConditionDetail.FOLDER_SIZE_GT: lambda v: f"(Get-ChildItem -Path $_.FullName -Recurse -File | Measure-Object -Property Length -Sum).Sum -gt {v}",
            FileConditionDetail.FOLDER_SIZE_LT: lambda v: f"(Get-ChildItem -Path $_.FullName -Recurse -File | Measure-Object -Property Length -Sum).Sum -lt {v}",
            FileConditionDetail.FOLDER_CREATION_TIME_GT: lambda v: f"$_.CreationTime -gt [datetime]'{v}'",
            FileConditionDetail.FOLDER_CREATION_TIME_LT: lambda v: f"$_.CreationTime -lt [datetime]'{v}'",
        }

        conditions = []
        for condition in block.condition:
            if not condition:
                continue
            for key, value in condition.items():
                if key in condition_map:
                    conditions.append(condition_map[key](value))

        return " -and ".join(conditions) if conditions else ""

    def _create_action_command(self, block: FileSystemBlock) -> str:
        """Creates the action command."""
        if block.action == FileSystemAction.RENAME:
            if block.target == FileSystemType.FILE:
                return (
                    "ForEach-Object { "
                    f"Rename-Item -Path $_.FullName -NewName ('{block.rename}' + $counter + $_.Extension); "
                    "$counter++ "
                    "}"
                )
            else:  # For FOLDER target
                return (
                    "ForEach-Object { "
                    f"Rename-Item -Path $_.FullName -NewName ('{block.rename}' + $counter); "
                    "$counter++ "
                    "}"
                )

        destination = f"'{block.destination}'" if block.destination else ""
        action_commands = {
            FileSystemAction.COPY: f"Copy-Item -Destination {destination}",
            FileSystemAction.MOVE: f"Move-Item -Destination {destination}",
            FileSystemAction.DELETE: "Remove-Item",
            FileSystemAction.COMPRESS: f"Compress-Archive -DestinationPath {self._get_archive_path(block)}",
            FileSystemAction.PRINT: (
                f"ForEach-Object {{ $_.FullName }} | "
                f"Out-File -FilePath '{block.destination}/file_list.txt' -Encoding UTF8"
            ),
        }
        return action_commands.get(block.action, "")

    def _get_archive_path(self, block: FileSystemBlock) -> str:
        """Generates the archive file path for Compress-Archive."""
        # Use a default archive name if none is provided
        archive_name = "archive.zip"
        # If destination includes a file name, use it
        if block.destination and block.destination.lower().endswith(".zip"):
            archive_path = f"'{block.destination}'"
        else:
            # Append the default archive name to the destination path
            separator = (
                "" if block.destination and block.destination.endswith("/") else "/"
            )
            archive_path = f"'{block.destination}{separator}{archive_name}'"
        return archive_path
