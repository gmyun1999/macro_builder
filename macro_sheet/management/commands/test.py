from timeit import timeit

from django.core.management.base import BaseCommand

from macro_sheet.domain.block_serializer import GenericSerializer


class Command(BaseCommand):
    help = "Benchmark GenericSerializer deserialization performance"

    def handle(self, *args, **kwargs):
        # Define all test cases

        condition_block_data = {
            "id": "cond001",
            "block_type": "BASE_CONDITION_BLOCK",
            "condition_type": "FILE",
            "detail_condition_type": ["file_extension"],
            "value": ".txt",
        }

        file_condition_block_data = {
            "id": "filecond001",
            "block_type": "FILE_CONDITION_BLOCK",
            "condition_type": "FILE",
            "detail_condition_type": ["file_size_gt"],
            "value": "1024",
        }

        control_block_data = {
            "id": "control001",
            "block_type": "BASE_CONTROL_BLOCK",
            "control_type": "while",
            "conditions": [
                {
                    "id": "cond002",
                    "block_type": "BASE_CONDITION_BLOCK",
                    "condition_type": "API",
                    "detail_condition_type": ["file_name_startswith"],
                    "value": "test_",
                }
            ],
            "body": [
                {
                    "id": "fileaction001",
                    "block_type": "FILE_ACTION_BLOCK",
                    "action": "copy",
                    "target_loc": "/source/path",
                    "target_detail": "file_name",
                    "replace_text": None,
                    "chmod_value": None,
                    "destination": "/destination/path",
                    "target": "FILE",
                },
                {"id": "simple002", "block_type": "BASE_BLOCK"},
            ],
        }

        # 추가 테스트 케이스
        large_field_block_data = {
            "id": "large001",
            "block_type": "BASE_BLOCK",
            "field1": "value1",
            "field2": 42,
            "field3": 3.14,
            "field4": True,
            "field5": "optional",
            "field6": ["list_item1", "list_item2"],
            "field7": {
                "id": "filecond002",
                "block_type": "FILE_CONDITION_BLOCK",
                "condition_type": "FILE",
                "detail_condition_type": ["file_owner"],
                "value": "admin",
            },
            "field8": [
                {
                    "id": "filecond003",
                    "block_type": "FILE_CONDITION_BLOCK",
                    "condition_type": "FILE",
                    "detail_condition_type": ["file_size_gt"],
                    "value": "2048",
                },
                {
                    "id": "fileaction002",
                    "block_type": "FILE_ACTION_BLOCK",
                    "action": "move",
                    "target_loc": "/source/path2",
                    "target_detail": "file_content",
                    "replace_text": "new_text",
                    "chmod_value": 755,
                    "destination": "/destination/path2",
                    "target": "FILE",
                },
            ],
            "field9": {
                "id": "filecond004",
                "block_type": "FILE_CONDITION_BLOCK",
                "condition_type": "FILE",
                "detail_condition_type": ["file_extension"],
                "value": ".log",
            },
            "field10": {
                "id": "control002",
                "block_type": "BASE_CONTROL_BLOCK",
                "control_type": "if",
                "conditions": [
                    {
                        "id": "cond003",
                        "block_type": "BASE_CONDITION_BLOCK",
                        "condition_type": "MOUSE",
                        "detail_condition_type": ["file_modification_time_gt"],
                        "value": "2021-01-01",
                    }
                ],
                "body": [
                    {
                        "id": "fileaction003",
                        "block_type": "FILE_ACTION_BLOCK",
                        "action": "delete",
                        "target_loc": "/temp/path",
                        "target_detail": "file_metadata",
                        "replace_text": None,
                        "chmod_value": None,
                        "destination": None,
                        "target": "FILE",
                    }
                ],
            },
        }
        control_block_data = {
            "id": "control001",
            "block_type": "BASE_CONTROL_BLOCK",
            "control_type": "while",
            "conditions": [
                {"id": "cond002", "block_type": "BASE_CONDITION_BLOCK"},
                {
                    "id": "filecond002",
                    "block_type": "FILE_CONDITION_BLOCK",
                    "condition_type": "FILE",
                    "detail_condition_type": ["file_owner"],
                    "value": "admin",
                },
            ],
            "body": [
                {
                    "id": "fileaction001",
                    "block_type": "FILE_ACTION_BLOCK",
                    "action": "copy",
                    "target_loc": "/source/path",
                    "target_detail": "file_name",
                    "replace_text": None,
                    "chmod_value": None,
                    "destination": "/destination/path",
                    "target": "FILE",
                },
                {"id": "simple002", "block_type": "BASE_BLOCK"},
            ],
        }
        nested_control_data = {
            "id": "control001",
            "block_type": "BASE_CONTROL_BLOCK",
            "control_type": "while",
            "conditions": [
                {"id": "cond002", "block_type": "BASE_CONDITION_BLOCK"},
                {
                    "id": "filecond002",
                    "block_type": "FILE_CONDITION_BLOCK",
                    "condition_type": "FILE",
                    "detail_condition_type": ["file_owner"],
                    "value": "admin",
                },
            ],
            "body": [
                {
                    "id": "control001",
                    "block_type": "BASE_CONTROL_BLOCK",
                    "control_type": "while",
                    "conditions": [
                        {"id": "cond002", "block_type": "BASE_CONDITION_BLOCK"},
                        {
                            "id": "filecond002",
                            "block_type": "FILE_CONDITION_BLOCK",
                            "condition_type": "FILE",
                            "detail_condition_type": ["file_owner"],
                            "value": "admin",
                        },
                    ],
                    "body": [
                        {
                            "id": "fileaction001",
                            "block_type": "FILE_ACTION_BLOCK",
                            "action": "copy",
                            "target_loc": "/source/path",
                            "target_detail": "file_name",
                            "replace_text": None,
                            "chmod_value": None,
                            "destination": "/destination/path",
                            "target": "FILE",
                        },
                        {"id": "simple002", "block_type": "BASE_BLOCK"},
                    ],
                },
                {
                    "id": "control001",
                    "block_type": "BASE_CONTROL_BLOCK",
                    "control_type": "while",
                    "conditions": [
                        {"id": "cond002", "block_type": "BASE_CONDITION_BLOCK"},
                        {
                            "id": "filecond002",
                            "block_type": "FILE_CONDITION_BLOCK",
                            "condition_type": "FILE",
                            "detail_condition_type": ["file_owner"],
                            "value": "admin",
                        },
                    ],
                    "body": [
                        {
                            "id": "fileaction001",
                            "block_type": "FILE_ACTION_BLOCK",
                            "action": "copy",
                            "target_loc": "/source/path",
                            "target_detail": "file_name",
                            "replace_text": None,
                            "chmod_value": None,
                            "destination": "/destination/path",
                            "target": "FILE",
                        },
                        {"id": "simple002", "block_type": "BASE_BLOCK"},
                    ],
                },
            ],
        }
        test_cases = {
            "Condition Block Case": condition_block_data,
            "File Condition Block Case": file_condition_block_data,
            "Control Block Case": control_block_data,
            "nested control block case": nested_control_data,
        }

        # Define number of iterations for benchmarking
        iterations = 1000

        # Define a list to store results
        results = []

        # Iterate through each test case
        for test_name, test_data in test_cases.items():
            # Define the custom serializer function
            def use_custom_serializer():
                serializer = GenericSerializer(test_data)
                if serializer.is_valid():
                    domain = serializer.to_domain_object()
                    return domain

                else:
                    return serializer.errors

            # Benchmark Custom Serializer
            custom_time = timeit(use_custom_serializer, number=iterations)

            # Append the results
            results.append(
                {
                    "Test Case": test_name,
                    "Custom Serializer Time (s)": custom_time,
                    "Faster Serializer": "Custom Serializer",  # Only one serializer is used
                }
            )

        # Display the results
        self.stdout.write("\nBenchmark Results:\n")
        self.stdout.write(
            f"{'Test Case':<25} {'Custom Serializer (s)':<25} {'Faster Serializer'}"
        )
        for result in results:
            self.stdout.write(
                f"{result['Test Case']:<25} {result['Custom Serializer Time (s)']:<25.6f} {result['Faster Serializer']}"
            )
