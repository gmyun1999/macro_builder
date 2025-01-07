# from django.core.management.base import BaseCommand

# from macro_sheet.domain.block.file_system_block.file_system_block import (
#     FileConditionDetail,
#     FileSystemBlock,
# )
# from macro_sheet.service.service.block_service import BlockService, PowerShellConverter


# class Command(BaseCommand):
#     def __init__(self):
#         self.style = self.Style()

#     class Style:
#         @staticmethod
#         def SUCCESS(text):
#             return text

#         @staticmethod
#         def ERROR(text):
#             return text

#     def stdout_write(self, text):
#         print(text)

#     def handle(self, *args, **kwargs):
#         # Define test cases (50 cases)
#         test_cases = [
#             # Each test case includes 'test_data' and 'expected_command'
#             # Case 1
#             {
#                 "test_data": {
#                     "block_type": "FILE_SYSTEM_BLOCK",
#                     "target": "FILE",
#                     "action": "COPY",
#                     "loc": "/C/user/documents/",
#                     "condition": [
#                         {FileConditionDetail.FILE_EXTENSION: "docx"},
#                         {FileConditionDetail.FILE_SIZE_GT: "1024"},
#                     ],
#                     "destination": "/C/user/backup",
#                     "rename": None,
#                 },
#                 "expected_command": "Get-ChildItem -Path '/C/user/documents/' -File | Where-Object { $_.Extension -eq '.docx' -and $_.Length -gt 1024 } | Copy-Item -Destination '/C/user/backup'",
#             },
#             # Case 2
#             {
#                 "test_data": {
#                     "block_type": "FILE_SYSTEM_BLOCK",
#                     "target": "FOLDER",
#                     "action": "DELETE",
#                     "loc": "/C/user/temp/",
#                     "condition": [{FileConditionDetail.FOLDER_SIZE_LT: "5000"}],
#                     "destination": None,
#                     "rename": None,
#                 },
#                 "expected_command": "Get-ChildItem -Path '/C/user/temp/' -Directory | Where-Object { (Get-ChildItem -Path $_.FullName -Recurse -File | Measure-Object -Property Length -Sum).Sum -lt 5000 } | Remove-Item",
#             },
#             # Case 3
#             {
#                 "test_data": {
#                     "block_type": "FILE_SYSTEM_BLOCK",
#                     "target": "FILE",
#                     "action": "DELETE",
#                     "loc": "/C/user/logs/",
#                     "condition": [{FileConditionDetail.FILE_SIZE_GT: "5000"}],
#                     "destination": None,
#                     "rename": None,
#                 },
#                 "expected_command": "Get-ChildItem -Path '/C/user/logs/' -File | Where-Object { $_.Length -gt 5000 } | Remove-Item",
#             },
#             # Case 4
#             {
#                 "test_data": {
#                     "block_type": "FILE_SYSTEM_BLOCK",
#                     "target": "FOLDER",
#                     "action": "MOVE",
#                     "loc": "/C/user/projects/",
#                     "condition": [
#                         {FileConditionDetail.FOLDER_CREATION_TIME_LT: "2021-01-01"}
#                     ],
#                     "destination": "/C/user/archive/",
#                     "rename": None,
#                 },
#                 "expected_command": "Get-ChildItem -Path '/C/user/projects/' -Directory | Where-Object { $_.CreationTime -lt [datetime]'2021-01-01' } | Move-Item -Destination '/C/user/archive/'",
#             },
#             # Case 5
#             {
#                 "test_data": {
#                     "block_type": "FILE_SYSTEM_BLOCK",
#                     "target": "FILE",
#                     "action": "PRINT",
#                     "loc": "/C/user/images/",
#                     "condition": [{FileConditionDetail.FILE_EXTENSION: "png"}],
#                     "destination": "/C/user/image_list",
#                     "rename": None,
#                 },
#                 "expected_command": "Get-ChildItem -Path '/C/user/images/' -File | Where-Object { $_.Extension -eq '.png' } | ForEach-Object { $_.FullName } | Out-File -FilePath '/C/user/image_list/file_list.txt' -Encoding UTF8",
#             },
#             # Case 6
#             {
#                 "test_data": {
#                     "block_type": "FILE_SYSTEM_BLOCK",
#                     "target": "FOLDER",
#                     "action": "COMPRESS",
#                     "loc": "/C/user/music/",
#                     "condition": [{FileConditionDetail.FOLDER_SIZE_GT: "1000000"}],
#                     "destination": "/C/user/compressed_music",
#                     "rename": None,
#                 },
#                 "expected_command": "Get-ChildItem -Path '/C/user/music/' -Directory | Where-Object { (Get-ChildItem -Path $_.FullName -Recurse -File | Measure-Object -Property Length -Sum).Sum -gt 1000000 } | Compress-Archive -DestinationPath '/C/user/compressed_music/archive.zip'",
#             },
#             # Case 7
#             {
#                 "test_data": {
#                     "block_type": "FILE_SYSTEM_BLOCK",
#                     "target": "FILE",
#                     "action": "COPY",
#                     "loc": "/C/user/videos/",
#                     "condition": [{FileConditionDetail.FILE_EXTENSION: "mp4"}],
#                     "destination": "/C/user/video_backup",
#                     "rename": None,
#                 },
#                 "expected_command": "Get-ChildItem -Path '/C/user/videos/' -File | Where-Object { $_.Extension -eq '.mp4' } | Copy-Item -Destination '/C/user/video_backup'",
#             },
#             # Case 8
#             {
#                 "test_data": {
#                     "block_type": "FILE_SYSTEM_BLOCK",
#                     "target": "FILE",
#                     "action": "MOVE",
#                     "loc": "/C/user/downloads/",
#                     "condition": [{FileConditionDetail.FILE_SIZE_LT: "2048"}],
#                     "destination": "/C/user/small_files",
#                     "rename": None,
#                 },
#                 "expected_command": "Get-ChildItem -Path '/C/user/downloads/' -File | Where-Object { $_.Length -lt 2048 } | Move-Item -Destination '/C/user/small_files'",
#             },
#             # Case 9
#             {
#                 "test_data": {
#                     "block_type": "FILE_SYSTEM_BLOCK",
#                     "target": "FOLDER",
#                     "action": "RENAME",
#                     "loc": "/C/user/old_projects/",
#                     "condition": [],
#                     "destination": None,
#                     "rename": "archived_",
#                 },
#                 "expected_command": "$counter = 1; Get-ChildItem -Path '/C/user/old_projects/' -Directory | ForEach-Object { Rename-Item -Path $_.FullName -NewName ('archived_' + $counter); $counter++ }",
#             },
#             # Case 10
#             {
#                 "test_data": {
#                     "block_type": "FILE_SYSTEM_BLOCK",
#                     "target": "FILE",
#                     "action": "DELETE",
#                     "loc": "/C/user/desktop/",
#                     "condition": [
#                         {FileConditionDetail.FILE_CREATION_TIME_LT: "2020-01-01"}
#                     ],
#                     "destination": None,
#                     "rename": None,
#                 },
#                 "expected_command": "Get-ChildItem -Path '/C/user/desktop/' -File | Where-Object { $_.CreationTime -lt [datetime]'2020-01-01' } | Remove-Item",
#             },
#             # Case 11
#             {
#                 "test_data": {
#                     "block_type": "FILE_SYSTEM_BLOCK",
#                     "target": "FOLDER",
#                     "action": "COPY",
#                     "loc": "/C/user/workspaces/",
#                     "condition": [{FileConditionDetail.NAME_STARTSWITH: "project_"}],
#                     "destination": "/C/user/projects_backup",
#                     "rename": None,
#                 },
#                 "expected_command": "Get-ChildItem -Path '/C/user/workspaces/' -Directory | Where-Object { $_.Name -like 'project_*' } | Copy-Item -Destination '/C/user/projects_backup'",
#             },
#             # Case 12
#             {
#                 "test_data": {
#                     "block_type": "FILE_SYSTEM_BLOCK",
#                     "target": "FILE",
#                     "action": "RENAME",
#                     "loc": "/C/user/pictures/",
#                     "condition": [{FileConditionDetail.FILE_EXTENSION: "jpg"}],
#                     "destination": None,
#                     "rename": "photo_",
#                 },
#                 "expected_command": "$counter = 1; Get-ChildItem -Path '/C/user/pictures/' -File | Where-Object { $_.Extension -eq '.jpg' } | ForEach-Object { Rename-Item -Path $_.FullName -NewName ('photo_' + $counter + $_.Extension); $counter++ }",
#             },
#             # Case 13
#             {
#                 "test_data": {
#                     "block_type": "FILE_SYSTEM_BLOCK",
#                     "target": "FILE",
#                     "action": "PRINT",
#                     "loc": "/C/user/scripts/",
#                     "condition": [{FileConditionDetail.NAME_ENDSWITH: "_backup"}],
#                     "destination": "/C/user/script_list",
#                     "rename": None,
#                 },
#                 "expected_command": "Get-ChildItem -Path '/C/user/scripts/' -File | Where-Object { $_.BaseName -like '*_backup' } | ForEach-Object { $_.FullName } | Out-File -FilePath '/C/user/script_list/file_list.txt' -Encoding UTF8",
#             },
#             # Case 14
#             {
#                 "test_data": {
#                     "block_type": "FILE_SYSTEM_BLOCK",
#                     "target": "FILE",
#                     "action": "COMPRESS",
#                     "loc": "/C/user/logs/",
#                     "condition": [{FileConditionDetail.FILE_SIZE_GT: "10000"}],
#                     "destination": "/C/user/compressed_logs/logs.zip",  # Updated to include archive file name
#                     "rename": None,
#                 },
#                 "expected_command": "Get-ChildItem -Path '/C/user/logs/' -File | Where-Object { $_.Length -gt 10000 } | Compress-Archive -DestinationPath '/C/user/compressed_logs/logs.zip'",
#             },
#             # Case 15
#             {
#                 "test_data": {
#                     "block_type": "FILE_SYSTEM_BLOCK",
#                     "target": "FILE",
#                     "action": "COMPRESS",
#                     "loc": "/C/user/logs/",
#                     "condition": [{FileConditionDetail.FILE_SIZE_GT: "10000"}],
#                     "destination": "/C/user/compressed_logs",
#                     "rename": None,
#                 },
#                 "expected_command": "Get-ChildItem -Path '/C/user/logs/' -File | Where-Object { $_.Length -gt 10000 } | Compress-Archive -DestinationPath '/C/user/compressed_logs/archive.zip'",
#             },
#             # Case 16
#             {
#                 "test_data": {
#                     "block_type": "FILE_SYSTEM_BLOCK",
#                     "target": "FOLDER",
#                     "action": "DELETE",
#                     "loc": "/C/user/old_data/",
#                     "condition": [{FileConditionDetail.FOLDER_SIZE_LT: "10000"}],
#                     "destination": None,
#                     "rename": None,
#                 },
#                 "expected_command": "Get-ChildItem -Path '/C/user/old_data/' -Directory | Where-Object { (Get-ChildItem -Path $_.FullName -Recurse -File | Measure-Object -Property Length -Sum).Sum -lt 10000 } | Remove-Item",
#             },
#             # Case 17
#             {
#                 "test_data": {
#                     "block_type": "FILE_SYSTEM_BLOCK",
#                     "target": "FILE",
#                     "action": "COPY",
#                     "loc": "/C/user/backup/",
#                     "condition": [],
#                     "destination": "/C/user/secondary_backup",
#                     "rename": None,
#                 },
#                 "expected_command": "Get-ChildItem -Path '/C/user/backup/' -File | Copy-Item -Destination '/C/user/secondary_backup'",
#             },
#             # Case 18
#             {
#                 "test_data": {
#                     "block_type": "FILE_SYSTEM_BLOCK",
#                     "target": "FILE",
#                     "action": "MOVE",
#                     "loc": "/C/user/data/",
#                     "condition": [{FileConditionDetail.NAME_STARTSWITH: "data_"}],
#                     "destination": "/C/user/data_archive",
#                     "rename": None,
#                 },
#                 "expected_command": "Get-ChildItem -Path '/C/user/data/' -File | Where-Object { $_.BaseName -like 'data_*' } | Move-Item -Destination '/C/user/data_archive'",
#             },
#             # Case 19
#             {
#                 "test_data": {
#                     "block_type": "FILE_SYSTEM_BLOCK",
#                     "target": "FOLDER",
#                     "action": "COPY",
#                     "loc": "/C/user/media/",
#                     "condition": [],
#                     "destination": "/C/user/media_backup",
#                     "rename": None,
#                 },
#                 "expected_command": "Get-ChildItem -Path '/C/user/media/' -Directory | Copy-Item -Destination '/C/user/media_backup'",
#             },
#             # Case 20
#             {
#                 "test_data": {
#                     "block_type": "FILE_SYSTEM_BLOCK",
#                     "target": "FILE",
#                     "action": "DELETE",
#                     "loc": "/C/user/cache/",
#                     "condition": [{FileConditionDetail.FILE_EXTENSION: "tmp"}],
#                     "destination": None,
#                     "rename": None,
#                 },
#                 "expected_command": "Get-ChildItem -Path '/C/user/cache/' -File | Where-Object { $_.Extension -eq '.tmp' } | Remove-Item",
#             },
#             # Case 21
#             {
#                 "test_data": {
#                     "block_type": "FILE_SYSTEM_BLOCK",
#                     "target": "FOLDER",
#                     "action": "RENAME",
#                     "loc": "/C/user/test_folders/",
#                     "condition": [{FileConditionDetail.NAME_ENDSWITH: "_test"}],
#                     "destination": None,
#                     "rename": "experiment_",
#                 },
#                 "expected_command": "$counter = 1; Get-ChildItem -Path '/C/user/test_folders/' -Directory | Where-Object { $_.Name -like '*_test' } | ForEach-Object { Rename-Item -Path $_.FullName -NewName ('experiment_' + $counter); $counter++ }",
#             },
#             # Case 22
#             {
#                 "test_data": {
#                     "block_type": "FILE_SYSTEM_BLOCK",
#                     "target": "FILE",
#                     "action": "COMPRESS",
#                     "loc": "/C/user/sounds/",
#                     "condition": [{FileConditionDetail.FILE_EXTENSION: "wav"}],
#                     "destination": "/C/user/compressed_sounds",
#                     "rename": None,
#                 },
#                 "expected_command": "Get-ChildItem -Path '/C/user/sounds/' -File | Where-Object { $_.Extension -eq '.wav' } | Compress-Archive -DestinationPath '/C/user/compressed_sounds/archive.zip'",
#             },
#             # Case 23
#             {
#                 "test_data": {
#                     "block_type": "FILE_SYSTEM_BLOCK",
#                     "target": "FOLDER",
#                     "action": "PRINT",
#                     "loc": "/C/user/documents/",
#                     "condition": [{FileConditionDetail.FOLDER_SIZE_GT: "20000"}],
#                     "destination": "/C/user/large_folders",
#                     "rename": None,
#                 },
#                 "expected_command": "Get-ChildItem -Path '/C/user/documents/' -Directory | Where-Object { (Get-ChildItem -Path $_.FullName -Recurse -File | Measure-Object -Property Length -Sum).Sum -gt 20000 } | ForEach-Object { $_.FullName } | Out-File -FilePath '/C/user/large_folders/file_list.txt' -Encoding UTF8",
#             },
#             # Case 24
#             {
#                 "test_data": {
#                     "block_type": "FILE_SYSTEM_BLOCK",
#                     "target": "FILE",
#                     "action": "COPY",
#                     "loc": "/C/user/downloads/",
#                     "condition": [
#                         {FileConditionDetail.FILE_CREATION_TIME_GT: "2021-12-31"}
#                     ],
#                     "destination": "/C/user/new_downloads",
#                     "rename": None,
#                 },
#                 "expected_command": "Get-ChildItem -Path '/C/user/downloads/' -File | Where-Object { $_.CreationTime -gt [datetime]'2021-12-31' } | Copy-Item -Destination '/C/user/new_downloads'",
#             },
#             # Case 25
#             {
#                 "test_data": {
#                     "block_type": "FILE_SYSTEM_BLOCK",
#                     "target": "FILE",
#                     "action": "MOVE",
#                     "loc": "/C/user/music/",
#                     "condition": [{FileConditionDetail.FILE_SIZE_LT: "5000"}],
#                     "destination": "/C/user/small_music_files",
#                     "rename": None,
#                 },
#                 "expected_command": "Get-ChildItem -Path '/C/user/music/' -File | Where-Object { $_.Length -lt 5000 } | Move-Item -Destination '/C/user/small_music_files'",
#             },
#             # Case 26
#             {
#                 "test_data": {
#                     "block_type": "FILE_SYSTEM_BLOCK",
#                     "target": "FOLDER",
#                     "action": "DELETE",
#                     "loc": "/C/user/unused/",
#                     "condition": [
#                         {FileConditionDetail.FOLDER_CREATION_TIME_LT: "2019-01-01"}
#                     ],
#                     "destination": None,
#                     "rename": None,
#                 },
#                 "expected_command": "Get-ChildItem -Path '/C/user/unused/' -Directory | Where-Object { $_.CreationTime -lt [datetime]'2019-01-01' } | Remove-Item",
#             },
#             # Case 27
#             {
#                 "test_data": {
#                     "block_type": "FILE_SYSTEM_BLOCK",
#                     "target": "FILE",
#                     "action": "RENAME",
#                     "loc": "/C/user/videos/",
#                     "condition": [{FileConditionDetail.NAME_STARTSWITH: "clip_"}],
#                     "destination": None,
#                     "rename": "video_",
#                 },
#                 "expected_command": "$counter = 1; Get-ChildItem -Path '/C/user/videos/' -File | Where-Object { $_.BaseName -like 'clip_*' } | ForEach-Object { Rename-Item -Path $_.FullName -NewName ('video_' + $counter + $_.Extension); $counter++ }",
#             },
#             # Case 28
#             {
#                 "test_data": {
#                     "block_type": "FILE_SYSTEM_BLOCK",
#                     "target": "FOLDER",
#                     "action": "MOVE",
#                     "loc": "/C/user/archives/",
#                     "condition": [{FileConditionDetail.FOLDER_SIZE_GT: "500000"}],
#                     "destination": "/C/user/large_archives",
#                     "rename": None,
#                 },
#                 "expected_command": "Get-ChildItem -Path '/C/user/archives/' -Directory | Where-Object { (Get-ChildItem -Path $_.FullName -Recurse -File | Measure-Object -Property Length -Sum).Sum -gt 500000 } | Move-Item -Destination '/C/user/large_archives'",
#             },
#             # Case 29
#             {
#                 "test_data": {
#                     "block_type": "FILE_SYSTEM_BLOCK",
#                     "target": "FILE",
#                     "action": "COMPRESS",
#                     "loc": "/C/user/documents/",
#                     "condition": [{FileConditionDetail.FILE_SIZE_GT: "2000"}],
#                     "destination": "/C/user/compressed_docs/archive.zip",  # Updated to include archive file name
#                     "rename": None,
#                 },
#                 "expected_command": "Get-ChildItem -Path '/C/user/documents/' -File | Where-Object { $_.Length -gt 2000 } | Compress-Archive -DestinationPath '/C/user/compressed_docs/archive.zip'",
#             },
#             # Case 30
#             {
#                 "test_data": {
#                     "block_type": "FILE_SYSTEM_BLOCK",
#                     "target": "FILE",
#                     "action": "COMPRESS",
#                     "loc": "/C/user/documents/",
#                     "condition": [{FileConditionDetail.FILE_SIZE_GT: "2000"}],
#                     "destination": "/C/user/compressed_docs",
#                     "rename": None,
#                 },
#                 "expected_command": "Get-ChildItem -Path '/C/user/documents/' -File | Where-Object { $_.Length -gt 2000 } | Compress-Archive -DestinationPath '/C/user/compressed_docs/archive.zip'",
#             },
#             # Continue adding cases up to Case 50
#             # ...
#             # Case 50
#             {
#                 "test_data": {
#                     "block_type": "FILE_SYSTEM_BLOCK",
#                     "target": "FILE",
#                     "action": "RENAME",
#                     "loc": "/C/user/music/",
#                     "condition": [{FileConditionDetail.NAME_ENDSWITH: "old"}],
#                     "destination": None,
#                     "rename": "classic",
#                 },
#                 "expected_command": "$counter = 1; Get-ChildItem -Path '/C/user/music/' -File | Where-Object { $_.BaseName -like '*old' } | ForEach-Object { Rename-Item -Path $_.FullName -NewName ('classic' + $counter + $_.Extension); $counter++ }",
#             },
#         ]

#         # Execute tests
#         for i, case in enumerate(test_cases, start=1):
#             self.stdout_write(f"\n--- Test Case {i} ---")
#             test_data = case["test_data"]
#             expected_command = case["expected_command"]
#             try:
#                 # Convert DTO to object
#                 filesystem_block = FileSystemBlock.from_dict(test_data)

#                 # Perform validation
#                 filesystem_block.validate()
#                 self.stdout_write(
#                     self.style.SUCCESS(f"Validation passed for case {i}.")
#                 )

#                 # Generate PowerShell command
#                 converter = PowerShellConverter()
#                 generated_command = converter.convert_fileblock_to_powershell(
#                     filesystem_block
#                 )

#                 # Compare with expected command
#                 if generated_command.strip() == expected_command.strip():
#                     self.stdout_write(
#                         self.style.SUCCESS(
#                             f"Command matches expected output for case {i}."
#                         )
#                     )
#                 else:
#                     self.stdout_write(
#                         self.style.ERROR(
#                             f"Command does not match expected output for case {i}."
#                         )
#                     )
#                     self.stdout_write(f"Generated Command:\n{generated_command}")
#                     self.stdout_write(f"Expected Command:\n{expected_command}")

#             except ValueError as e:
#                 self.stdout_write(
#                     self.style.ERROR(f"Validation failed for case {i}: {e}")
#                 )
#             except Exception as e:
#                 self.stdout_write(self.style.ERROR(f"Error in case {i}: {e}"))

#     def stdout_write(self, text):
#         print(text)
