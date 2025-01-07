# from django.core.management.base import BaseCommand

# from macro_sheet.domain.block.base_block.loop_block import LoopBlock
# from macro_sheet.domain.block.base_block.main_block import MainBlock
# from macro_sheet.domain.block.base_block.reference_block import ReferenceBlock
# from macro_sheet.domain.block.block import BlockType
# from macro_sheet.domain.block.file_system_block.file_system_block import (
#     FileConditionDetail,
#     FileSystemAction,
#     FileSystemBlock,
#     FileSystemType,
# )
# from macro_sheet.domain.Function.block_function import BlockFunction
# from macro_sheet.domain.worksheet.worksheet import Worksheet
# from macro_sheet.service.service.block_service import BlockService


# class Command(BaseCommand):
#     def handle(self, *args, **kwargs):
#         # Initialize BlockService
#         service = BlockService()

#         # 테스트 케이스 구현

#         # Define BlockFunctions
#         nested_function_1 = BlockFunction(
#             id="func_nested_1",
#             owner_id="user1",
#             name="NestedFunction1",
#             blocks=[
#                 LoopBlock(
#                     iter_cnt="2",
#                     body=[
#                         FileSystemBlock(
#                             target=FileSystemType.FILE,
#                             action=FileSystemAction.DELETE,
#                             loc="/C/user/temp/",
#                             condition=[{FileConditionDetail.FILE_SIZE_GT: "1000"}],
#                             destination=None,
#                             rename=None,
#                         ),
#                         FileSystemBlock(
#                             target=FileSystemType.FILE,
#                             action=FileSystemAction.PRINT,
#                             loc="/C/user/images/",
#                             condition=[{FileConditionDetail.FILE_EXTENSION: "jpg"}],
#                             destination="/C/user/image_list",
#                             rename=None,
#                         ),
#                     ],
#                 )
#             ],
#         )

#         nested_function_2 = BlockFunction(
#             id="func_nested_2",
#             owner_id="user1",
#             name="NestedFunction2",
#             blocks=[
#                 FileSystemBlock(
#                     target=FileSystemType.FILE,
#                     action=FileSystemAction.COMPRESS,
#                     loc="/C/user/logs/",
#                     condition=[{FileConditionDetail.FILE_EXTENSION: "log"}],
#                     destination="/C/user/compressed_logs/logs.zip",
#                     rename=None,
#                 )
#             ],
#         )

#         nested_function_3 = BlockFunction(
#             id="func_nested_3",
#             owner_id="user1",
#             name="NestedFunction3",
#             blocks=[
#                 LoopBlock(
#                     iter_cnt="2",
#                     body=[
#                         FileSystemBlock(
#                             target=FileSystemType.FILE,
#                             action=FileSystemAction.DELETE,
#                             loc="/C/user/temp/",
#                             condition=[{FileConditionDetail.FILE_SIZE_GT: "500"}],
#                             destination=None,
#                             rename=None,
#                         )
#                     ],
#                 )
#             ],
#         )

#         block_functions = [nested_function_1, nested_function_2, nested_function_3]

#         # Prepare the Worksheet with complex blocks
#         main_block2 = MainBlock(
#             body=[
#                 LoopBlock(
#                     iter_cnt="2",
#                     body=[
#                         # First FileSystemBlock in the outer loop
#                         FileSystemBlock(
#                             target=FileSystemType.FILE,
#                             action=FileSystemAction.COPY,
#                             loc="/C/user/documents/",
#                             condition=[{FileConditionDetail.FILE_EXTENSION: "txt"}],
#                             destination="/C/user/backup",
#                             rename=None,
#                         ),
#                         # Nested LoopBlock inside the main LoopBlock
#                         LoopBlock(
#                             iter_cnt="3",
#                             body=[
#                                 # Reference to nested_function_1 containing its own nested loop
#                                 ReferenceBlock(
#                                     reference_id="func_nested_1",
#                                 ),
#                                 # Another FileSystemBlock in this inner loop
#                                 FileSystemBlock(
#                                     target=FileSystemType.FILE,
#                                     action=FileSystemAction.MOVE,
#                                     loc="/C/user/downloads/",
#                                     condition=[
#                                         {FileConditionDetail.NAME_ENDSWITH: "_old"}
#                                     ],
#                                     destination="/C/user/old_downloads/",
#                                     rename=None,
#                                 ),
#                             ],
#                         ),
#                         # Reference to another function at the end of the main loop
#                         ReferenceBlock(
#                             reference_id="func_nested_2",
#                         ),
#                     ],
#                 )
#             ]
#         )
#         worksheet = Worksheet(
#             id="ws1", name="TestWorksheet", owner_id="user1", main_block=main_block2
#         )

#         # Define additional BlockFunctions for complex tests
#         block_function_3 = nested_function_3
#         # block_functions already includes block_function_3

#         # 테스트 케이스 목록
#         tests = [
#             # Test 1: FileSystemBlock COPY action
#             {
#                 "name": "Test 1: FileSystemBlock COPY action",
#                 "command": service.convert_file_system_block_to_str_code(
#                     fs_block_1 := FileSystemBlock(
#                         target=FileSystemType.FILE,
#                         action=FileSystemAction.COPY,
#                         loc="/C/user/documents/",
#                         condition=[{FileConditionDetail.FILE_EXTENSION: "txt"}],
#                         destination="/C/user/backup",
#                         rename=None,
#                     )
#                 ),
#             },
#             # Test 2: FileSystemBlock RENAME action
#             {
#                 "name": "Test 2: FileSystemBlock RENAME action",
#                 "command": service.convert_file_system_block_to_str_code(
#                     fs_block_2 := FileSystemBlock(
#                         target=FileSystemType.FOLDER,
#                         action=FileSystemAction.RENAME,
#                         loc="/C/user/projects/",
#                         condition=[{FileConditionDetail.NAME_STARTSWITH: "old_"}],
#                         destination=None,
#                         rename="archived_",
#                     )
#                 ),
#             },
#             # Test 3: FileSystemBlock DELETE action
#             {
#                 "name": "Test 3: FileSystemBlock DELETE action",
#                 "command": service.convert_file_system_block_to_str_code(
#                     fs_block_3 := FileSystemBlock(
#                         target=FileSystemType.FILE,
#                         action=FileSystemAction.DELETE,
#                         loc="/C/user/temp/",
#                         condition=[{FileConditionDetail.FILE_SIZE_GT: "1000"}],
#                         destination=None,
#                         rename=None,
#                     )
#                 ),
#             },
#             # Test 4: FileSystemBlock COMPRESS action
#             {
#                 "name": "Test 4: FileSystemBlock COMPRESS action",
#                 "command": service.convert_file_system_block_to_str_code(
#                     fs_block_4 := FileSystemBlock(
#                         target=FileSystemType.FILE,
#                         action=FileSystemAction.COMPRESS,
#                         loc="/C/user/logs/",
#                         condition=[{FileConditionDetail.FILE_EXTENSION: "log"}],
#                         destination="/C/user/compressed_logs/logs.zip",
#                         rename=None,
#                     )
#                 ),
#             },
#             # Test 5: FileSystemBlock MOVE action
#             {
#                 "name": "Test 5: FileSystemBlock MOVE action",
#                 "command": service.convert_file_system_block_to_str_code(
#                     fs_block_5 := FileSystemBlock(
#                         target=FileSystemType.FILE,
#                         action=FileSystemAction.MOVE,
#                         loc="/C/user/downloads/",
#                         condition=[{FileConditionDetail.NAME_ENDSWITH: "_old"}],
#                         destination="/C/user/old_downloads/",
#                         rename=None,
#                     )
#                 ),
#             },
#             # Test 6: FileSystemBlock with MOVE action and NAME_ENDSWITH condition
#             {
#                 "name": "Test 6: FileSystemBlock with MOVE action and NAME_ENDSWITH condition",
#                 "command": service.convert_file_system_block_to_str_code(fs_block_5),
#             },
#             # Test 7: LoopBlock with mixed actions
#             {
#                 "name": "Test 7: LoopBlock with mixed actions",
#                 "command": service.convert_loop_block_to_str_code(
#                     loop_block_mixed := LoopBlock(
#                         iter_cnt="3",
#                         body=[fs_block_1, fs_block_4, fs_block_5],
#                     ),
#                     block_functions,
#                 ),
#             },
#             # Test 8: ReferenceBlock containing LoopBlock
#             {
#                 "name": "Test 8: ReferenceBlock containing LoopBlock",
#                 "command": service.render_reference_block_to_str_code(
#                     reference_block_1 := ReferenceBlock(
#                         reference_id="func_nested_1",
#                     ),
#                     block_functions,
#                 ),
#             },
#             # Test 9: LoopBlock with nested ReferenceBlock containing LoopBlock
#             {
#                 "name": "Test 9: LoopBlock with nested ReferenceBlock containing LoopBlock",
#                 "command": service.convert_loop_block_to_str_code(
#                     loop_block_complex := LoopBlock(
#                         iter_cnt="2",
#                         body=[
#                             reference_block_3 := ReferenceBlock(
#                                 reference_id="func_nested_3",
#                             ),
#                             fs_block_5,
#                         ],
#                     ),
#                     block_functions,
#                 ),
#             },
#             # Test 10: FileSystemBlock with PRINT action
#             {
#                 "name": "Test 10: FileSystemBlock with PRINT action",
#                 "command": service.convert_file_system_block_to_str_code(
#                     fs_block_6 := FileSystemBlock(
#                         target=FileSystemType.FILE,
#                         action=FileSystemAction.PRINT,
#                         loc="/C/user/images/",
#                         condition=[{FileConditionDetail.FILE_EXTENSION: "jpg"}],
#                         destination="/C/user/image_list",
#                         rename=None,
#                     )
#                 ),
#             },
#             # Test 12: LoopBlock with high iteration count
#             {
#                 "name": "Test 12: LoopBlock with high iteration count",
#                 "command": service.convert_loop_block_to_str_code(
#                     loop_block_high_iter := LoopBlock(
#                         iter_cnt="100",
#                         body=[fs_block_1],
#                     ),
#                     block_functions,
#                 ),
#             },
#             # Test 13: Deeply nested LoopBlocks
#             {
#                 "name": "Test 13: Deeply nested LoopBlocks",
#                 "command": service.convert_loop_block_to_str_code(
#                     deeply_nested_loop := LoopBlock(
#                         iter_cnt="2",
#                         body=[
#                             LoopBlock(
#                                 iter_cnt="2",
#                                 body=[
#                                     LoopBlock(
#                                         iter_cnt="2",
#                                         body=[fs_block_1],
#                                     )
#                                 ],
#                             )
#                         ],
#                     ),
#                     block_functions,
#                 ),
#             },
#         ]

#         # Execute tests
#         for test in tests:
#             print(f"\n=== {test['name']} ===")
#             try:
#                 if test.get("setup"):
#                     # 설정 함수 실행
#                     for setup_action in test["setup"]:
#                         setup_action()
#                 if test.get("command") is not None:
#                     generated_command = test["command"]
#                     print("Generated Command:")
#                     print(generated_command)
#                 if test.get("expected_exception"):
#                     # 순환 참조 테스트
#                     try:
#                         # 스크립트 생성 시도
#                         service.generate_script_from_worksheet(
#                             worksheet, block_functions
#                         )
#                         print("Test Result: FAIL (Cyclic reference not detected)")
#                     except Exception as e:
#                         if isinstance(e, test["expected_exception"]):
#                             print(f"Test Result: PASS (Caught expected exception: {e})")
#                         else:
#                             print(
#                                 f"Test Result: FAIL (Caught unexpected exception: {e})"
#                             )
#                 else:
#                     # 일반적인 테스트 케이스
#                     print("Test Result: PASS")
#             except Exception as e:
#                 print(f"Test Result: FAIL (Exception occurred: {e})")
#                 from traceback import format_exc

#                 print("Exception details:")
#                 print(format_exc())

#         # 생성된 스크립트를 파일로 저장
#         generated_script = service.generate_script_from_worksheet(
#             worksheet, block_functions
#         )
#         with open("generated_script.py", "w") as f:
#             f.write(generated_script)

#         print("\nGenerated script has been written to 'generated_script.py'.")

#         main_block1_without_refer = MainBlock(
#             body=[
#                 LoopBlock(
#                     iter_cnt="3",
#                     body=[
#                         # Another FileSystemBlock in this inner loop
#                         FileSystemBlock(
#                             target=FileSystemType.FILE,
#                             action=FileSystemAction.MOVE,
#                             loc="/C/user/downloads/",
#                             condition=[{FileConditionDetail.NAME_ENDSWITH: "_old"}],
#                             destination="/C/user/old_downloads/",
#                             rename=None,
#                         ),
#                         LoopBlock(
#                             iter_cnt="3",
#                             body=[
#                                 # Another FileSystemBlock in this inner loop
#                                 FileSystemBlock(
#                                     target=FileSystemType.FILE,
#                                     action=FileSystemAction.MOVE,
#                                     loc="/C/user/downloads/",
#                                     condition=[
#                                         {FileConditionDetail.NAME_ENDSWITH: "_old"}
#                                     ],
#                                     destination="/C/user/old_downloads/",
#                                     rename=None,
#                                 ),
#                             ],
#                         ),
#                     ],
#                 ),
#             ]
#         )

#         main_block1 = MainBlock(
#             body=[
#                 LoopBlock(
#                     iter_cnt="2",
#                     body=[
#                         # First FileSystemBlock in the outer loop
#                         FileSystemBlock(
#                             target=FileSystemType.FILE,
#                             action=FileSystemAction.COPY,
#                             loc="/C/user/documents/",
#                             condition=[{FileConditionDetail.FILE_EXTENSION: "txt"}],
#                             destination="/C/user/backup",
#                             rename=None,
#                         ),
#                         # Nested LoopBlock inside the main LoopBlock
#                         LoopBlock(
#                             iter_cnt="3",
#                             body=[
#                                 # Reference to nested_function_1 containing its own nested loop
#                                 ReferenceBlock(
#                                     reference_id="func_nested_1",
#                                 ),
#                                 # Another FileSystemBlock in this inner loop
#                                 FileSystemBlock(
#                                     target=FileSystemType.FILE,
#                                     action=FileSystemAction.MOVE,
#                                     loc="/C/user/downloads/",
#                                     condition=[
#                                         {FileConditionDetail.NAME_ENDSWITH: "_old"}
#                                     ],
#                                     destination="/C/user/old_downloads/",
#                                     rename=None,
#                                 ),
#                             ],
#                         ),
#                         LoopBlock(
#                             iter_cnt="3",
#                             body=[
#                                 # Reference to nested_function_1 containing its own nested loop
#                                 ReferenceBlock(
#                                     reference_id="func_nested_1",
#                                 ),
#                                 # Another FileSystemBlock in this inner loop
#                                 FileSystemBlock(
#                                     target=FileSystemType.FILE,
#                                     action=FileSystemAction.MOVE,
#                                     loc="/C/user/downloads/",
#                                     condition=[
#                                         {FileConditionDetail.NAME_ENDSWITH: "_old"}
#                                     ],
#                                     destination="/C/user/old_downloads/",
#                                     rename=None,
#                                 ),
#                             ],
#                         ),
#                         LoopBlock(
#                             iter_cnt="3",
#                             body=[
#                                 # Reference to nested_function_1 containing its own nested loop
#                                 ReferenceBlock(
#                                     reference_id="func_nested_2",
#                                 ),
#                                 # Another FileSystemBlock in this inner loop
#                                 FileSystemBlock(
#                                     target=FileSystemType.FILE,
#                                     action=FileSystemAction.MOVE,
#                                     loc="/C/user/downloads/",
#                                     condition=[
#                                         {FileConditionDetail.NAME_ENDSWITH: "_old"}
#                                     ],
#                                     destination="/C/user/old_downloads/",
#                                     rename=None,
#                                 ),
#                             ],
#                         ),
#                         # Reference to another function at the end of the main loop
#                         ReferenceBlock(
#                             reference_id="func_nested_2",
#                         ),
#                     ],
#                 )
#             ]
#         )
#         worksheet = Worksheet(
#             id="ws1", name="TestWorksheet", owner_id="user1", main_block=main_block1
#         )
#         worksheet_without_refer = Worksheet(
#             id="ws_without_refer",
#             name="TestWorksheet_without_refer",
#             owner_id=None,
#             main_block=main_block1_without_refer,
#         )

#         # Test Case for Worksheet Script Generation
#         try:
#             print("\n=== Test 14: Worksheet Full Script Generation ===")
#             generated_script = service.generate_script_from_worksheet(
#                 worksheet, block_functions
#             )
#             print("Generated Script:")
#             print(generated_script)
#             print("Test Result: PASS")
#         except Exception as e:
#             print("Test Result: FAIL (Exception occurred: {}")
#             from traceback import format_exc

#             print("Exception details:")
#             print(format_exc())

#         # Save the generated script to a file
#         with open("generated_script.py", "w") as f:
#             f.write(generated_script)

#         print("\nGenerated script has been written to 'generated_script.py'.")

#         try:
#             print("\n=== Test 15: Worksheet Full Script Generation ===")
#             generated_script = service.generate_script_from_worksheet(
#                 worksheet=worksheet_without_refer, block_functions=[]
#             )
#             print("Generated Script:")
#             print(generated_script)
#             print("Test Result: PASS")
#         except Exception as e:
#             print("Test Result: FAIL (Exception occurred: {}")
#             from traceback import format_exc

#             print("Exception details:")
#             print(format_exc())

#         # Save the generated script to a file
#         with open("generated_script1.py", "w") as f:
#             f.write(generated_script)
