# # blocks/management/commands/test_converter.py

# import json
# from typing import Any, Dict

# from django.core.management.base import BaseCommand

# from macro_sheet.domain.block.base_block.condition_block import ConditionBlock
# from macro_sheet.domain.block.base_block.loop_block import LoopBlock
# from macro_sheet.domain.block.base_block.main_block import MainBlock
# from macro_sheet.domain.block.base_block.reference_block import ReferenceBlock
# from macro_sheet.domain.block.file_system_block.file_system_block import (
#     FileConditionDetail,
#     FileSystemAction,
#     FileSystemBlock,
#     FileSystemType,
# )

# # 도메인 클래스 임포트
# from macro_sheet.domain.Function.block_function import BlockFunction
# from macro_sheet.domain.worksheet.worksheet import Worksheet


# class Command(BaseCommand):
#     help = "Test DomainConverter for Worksheets and Blocks"

#     def handle(self, *args, **kwargs):
#         # 테스트 케이스 정의
#         test_cases = [
#             {
#                 "name": "Empty Worksheet with None main_block",
#                 "object": Worksheet(
#                     id="ws_empty_none",
#                     name="Empty Worksheet None",
#                     owner_id=None,
#                     main_block=None,
#                     blocks=[],
#                 ),
#             },
#             {
#                 "name": "Empty Worksheet with MainBlock",
#                 "object": Worksheet(
#                     id="ws_empty",
#                     name="Empty Worksheet",
#                     owner_id=None,
#                     main_block=MainBlock(body=[]),
#                     blocks=[],
#                 ),
#             },
#             {
#                 "name": "Empty Worksheet with empty MainBlock",
#                 "object": Worksheet(
#                     id="ws_empty",
#                     name="Empty Worksheet",
#                     owner_id=None,
#                     main_block=None,
#                     blocks=[],
#                 ),
#             },
#             {
#                 "name": "Worksheet with single FileSystemBlock",
#                 "object": Worksheet(
#                     id="ws_single_block",
#                     name="Single Block Worksheet",
#                     owner_id="owner1",
#                     main_block=MainBlock(
#                         body=[
#                             FileSystemBlock(
#                                 target=FileSystemType.FILE,
#                                 action=FileSystemAction.COPY,
#                                 loc="/path/source",
#                                 condition=[
#                                     {FileConditionDetail.NAME_STARTSWITH: "example.txt"}
#                                 ],
#                                 destination="/path/dest",
#                                 rename=None,
#                             )
#                         ]
#                     ),
#                     blocks=[],
#                 ),
#             },
#             {
#                 "name": "Worksheet with multiple FileSystemBlock",
#                 "object": Worksheet(
#                     id="ws_single_block",
#                     name="Single Block Worksheet",
#                     owner_id="owner1",
#                     main_block=MainBlock(
#                         body=[
#                             FileSystemBlock(
#                                 target=FileSystemType.FILE,
#                                 action=FileSystemAction.COPY,
#                                 loc="/path/source",
#                                 condition=[
#                                     {FileConditionDetail.NAME_STARTSWITH: "example.txt"}
#                                 ],
#                                 destination="/path/dest",
#                                 rename=None,
#                             ),
#                             FileSystemBlock(
#                                 target=FileSystemType.FILE,
#                                 action=FileSystemAction.COPY,
#                                 loc="/path/source",
#                                 condition=[
#                                     {FileConditionDetail.NAME_STARTSWITH: "example.txt"}
#                                 ],
#                                 destination="/path/dest",
#                                 rename=None,
#                             ),
#                             FileSystemBlock(
#                                 target=FileSystemType.FILE,
#                                 action=FileSystemAction.COPY,
#                                 loc="/path/source",
#                                 condition=[
#                                     {FileConditionDetail.NAME_STARTSWITH: "example.txt"}
#                                 ],
#                                 destination="/path/dest",
#                                 rename=None,
#                             ),
#                             FileSystemBlock(
#                                 target=FileSystemType.FILE,
#                                 action=FileSystemAction.COPY,
#                                 loc="/path/source",
#                                 condition=[
#                                     {FileConditionDetail.NAME_STARTSWITH: "example.txt"}
#                                 ],
#                                 destination="/path/dest",
#                                 rename=None,
#                             ),
#                         ]
#                     ),
#                     blocks=[],
#                 ),
#             },
#             {
#                 "name": "Worksheet with nested LoopBlock",
#                 "object": Worksheet(
#                     id="ws_nested_loop",
#                     name="Nested Loop Worksheet",
#                     owner_id="owner2",
#                     main_block=MainBlock(
#                         body=[
#                             ReferenceBlock(
#                                 reference_id="ref1",
#                                 reference_function_name="SomeFunction",
#                             ),
#                             LoopBlock(
#                                 iter_cnt="3",
#                                 body=[
#                                     FileSystemBlock(
#                                         target=FileSystemType.FOLDER,
#                                         action=FileSystemAction.DELETE,
#                                         loc="/path/folder",
#                                         condition=[
#                                             {
#                                                 FileConditionDetail.FOLDER_SIZE_GT: "100MB"
#                                             }
#                                         ],
#                                         destination=None,
#                                         rename=None,
#                                     ),
#                                     LoopBlock(
#                                         iter_cnt="2",
#                                         body=[
#                                             FileSystemBlock(
#                                                 target=FileSystemType.FILE,
#                                                 action=FileSystemAction.RENAME,
#                                                 loc="/path/file",
#                                                 condition=[
#                                                     {
#                                                         FileConditionDetail.NAME_STARTSWITH: "test"
#                                                     }
#                                                 ],
#                                                 destination=None,
#                                                 rename="new_name.txt",
#                                             ),
#                                             FileSystemBlock(
#                                                 target=FileSystemType.FILE,
#                                                 action=FileSystemAction.RENAME,
#                                                 loc="/path/file",
#                                                 condition=[
#                                                     {
#                                                         FileConditionDetail.NAME_STARTSWITH: "test"
#                                                     }
#                                                 ],
#                                                 destination=None,
#                                                 rename="new_name.txt",
#                                             ),
#                                             LoopBlock(
#                                                 iter_cnt="3",
#                                                 body=[
#                                                     ReferenceBlock(
#                                                         reference_id="ref1",
#                                                         reference_function_name="SomeFunction",
#                                                     ),
#                                                     FileSystemBlock(
#                                                         target=FileSystemType.FOLDER,
#                                                         action=FileSystemAction.DELETE,
#                                                         loc="/path/folder",
#                                                         condition=[
#                                                             {
#                                                                 FileConditionDetail.FOLDER_SIZE_GT: "100MB"
#                                                             }
#                                                         ],
#                                                         destination=None,
#                                                         rename=None,
#                                                     ),
#                                                     LoopBlock(
#                                                         iter_cnt="2",
#                                                         body=[
#                                                             FileSystemBlock(
#                                                                 target=FileSystemType.FILE,
#                                                                 action=FileSystemAction.RENAME,
#                                                                 loc="/path/file",
#                                                                 condition=[
#                                                                     {
#                                                                         FileConditionDetail.NAME_STARTSWITH: "test"
#                                                                     }
#                                                                 ],
#                                                                 destination=None,
#                                                                 rename="new_name.txt",
#                                                             ),
#                                                             FileSystemBlock(
#                                                                 target=FileSystemType.FILE,
#                                                                 action=FileSystemAction.RENAME,
#                                                                 loc="/path/file",
#                                                                 condition=[
#                                                                     {
#                                                                         FileConditionDetail.NAME_STARTSWITH: "test"
#                                                                     }
#                                                                 ],
#                                                                 destination=None,
#                                                                 rename="new_name.txt",
#                                                             ),
#                                                         ],
#                                                     ),
#                                                 ],
#                                             ),
#                                         ],
#                                     ),
#                                 ],
#                             ),
#                         ]
#                     ),
#                     blocks=[],
#                 ),
#             },
#             {
#                 "name": "BlockFunction with multiple blocks",
#                 "object": BlockFunction(
#                     id="bf1",
#                     owner_id="owner3",
#                     name="Sample Function",
#                     blocks=[
#                         FileSystemBlock(
#                             target=FileSystemType.FILE,
#                             action=FileSystemAction.MOVE,
#                             loc="/path/move_source",
#                             condition=[{FileConditionDetail.FILE_SIZE_GT: "10MB"}],
#                             destination="/path/move_dest",
#                             rename=None,
#                         ),
#                         LoopBlock(
#                             iter_cnt="2",
#                             body=[
#                                 FileSystemBlock(
#                                     target=FileSystemType.FILE,
#                                     action=FileSystemAction.RENAME,
#                                     loc="/path/file",
#                                     condition=[
#                                         {FileConditionDetail.NAME_STARTSWITH: "test"}
#                                     ],
#                                     destination=None,
#                                     rename="new_name.txt",
#                                 ),
#                                 FileSystemBlock(
#                                     target=FileSystemType.FILE,
#                                     action=FileSystemAction.RENAME,
#                                     loc="/path/file",
#                                     condition=[
#                                         {FileConditionDetail.NAME_STARTSWITH: "test"}
#                                     ],
#                                     destination=None,
#                                     rename="new_name.txt",
#                                 ),
#                             ],
#                         ),
#                         ReferenceBlock(
#                             reference_id="ref1", reference_function_name="SomeFunction"
#                         ),
#                     ],
#                 ),
#             },
#             {
#                 "name": "Worksheet with multiple block types",
#                 "object": Worksheet(
#                     id="ws_mixed_blocks",
#                     name="Mixed Blocks Worksheet",
#                     owner_id="owner4",
#                     main_block=MainBlock(
#                         body=[
#                             FileSystemBlock(
#                                 target=FileSystemType.FILE,
#                                 action=FileSystemAction.COMPRESS,
#                                 loc="/path/compress",
#                                 condition=[
#                                     {FileConditionDetail.FILE_EXTENSION: ".log"}
#                                 ],
#                                 destination=None,
#                                 rename=None,
#                             ),
#                             ConditionBlock(position=("0", "0")),
#                         ]
#                     ),
#                     blocks=[
#                         ReferenceBlock(
#                             reference_id="ref2",
#                             reference_function_name="AnotherFunction",
#                         )
#                     ],
#                 ),
#             },
#         ]

#         # 테스트 케이스 실행
#         for test_case in test_cases:
#             name = test_case["name"]
#             obj = test_case["object"]
#             self.stdout.write(f"--- Testing: {name} ---")

#             # 도메인 객체를 dict로 직렬화
#             try:
#                 obj_dict = obj.to_dict()
#                 obj_json = json.dumps(obj_dict, indent=4, ensure_ascii=False)
#                 self.stdout.write("Serialized to dict:")
#                 self.stdout.write(obj_json)
#             except Exception as e:
#                 self.stderr.write(self.style.ERROR(f"Serialization failed: {e}\n"))
#                 continue

#             # dict를 도메인 객체로 역직렬화
#             try:
#                 if isinstance(obj, Worksheet):
#                     deserialized_obj = Worksheet.from_dict(obj_dict)
#                 elif isinstance(obj, BlockFunction):
#                     deserialized_obj = BlockFunction.from_dict(obj_dict)
#                 else:
#                     raise ValueError(
#                         "Unsupported domain object type for deserialization"
#                     )

#                 self.stdout.write("Deserialized back to domain object:")
#                 self.stdout.write(str(deserialized_obj))
#             except Exception as e:
#                 self.stderr.write(self.style.ERROR(f"Deserialization failed: {e}\n"))
#                 continue

#             # 원본 객체와 역직렬화된 객체 비교
#             try:
#                 if deserialized_obj == obj:
#                     self.stdout.write(
#                         self.style.SUCCESS(
#                             "Test passed: Deserialized object matches the original.\n"
#                         )
#                     )
#                 else:
#                     self.stderr.write(
#                         self.style.ERROR(
#                             "Test failed: Deserialized object does not match the original.\n"
#                         )
#                     )
#             except Exception as e:
#                 self.stderr.write(self.style.ERROR(f"Comparison failed: {e}\n"))

#         self.stdout.write(self.style.SUCCESS("All tests completed."))
