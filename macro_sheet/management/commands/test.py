from timeit import timeit

from django.core.management.base import BaseCommand

from macro_sheet.domain.block_serializer import GenericSerializer


class Command(BaseCommand):
    help = "Benchmark GenericSerializer deserialization performance"

    def handle(self, *args, **kwargs):
        # Define all test cases

        condition_block_data = {"id": "cond001", "block_type": "BASE_CONDITION_BLOCK"}

        file_condition_block_data = {
            "id": "filecond001",
            "block_type": "FILE_CONDITION_BLOCK",
            "condition_type": "FILE",
            "detail_condition_type": ["FILE_SIZE_GT"],
            "value": "1024",
        }

        control_block_data = {
            "id": "control001",
            "block_type": "BASE_CONTROL_BLOCK",
            "control_type": "WHILE",
            "conditions": [
                {"id": "cond002", "block_type": "BASE_CONDITION_BLOCK"},
                {
                    "id": "filecond002",
                    "block_type": "FILE_CONDITION_BLOCK",
                    "condition_type": "FILE",
                    "detail_condition_type": ["FILE_OWNER"],
                    "value": "admin",
                },
            ],
            "body": [
                {
                    "id": "fileaction001",
                    "block_type": "FILE_ACTION_BLOCK",
                    "action": "COPY",
                    "target_loc": "/source/path",
                    "target_detail": "FILE_NAME",
                    "replace_text": None,
                    "chmod_value": None,
                    "destination": "/destination/path",
                    "target": "FILE",
                },
                {
                    "id": "fileaction001",
                    "block_type": "FILE_ACTION_BLOCK",
                    "action": "COPY",
                    "target_loc": "/source/path",
                    "target_detail": "FILE_NAME",
                    "replace_text": None,
                    "chmod_value": None,
                    "destination": "/destination/path",
                    "target": "FILE",
                },
            ],
        }
        action_block = {
            "id": "fileaction001",
            "block_type": "FILE_ACTION_BLOCK",
            "action": "COPY",
            "target_loc": "/source/path",
            "target_detail": "FILE_NAME",
            "replace_text": None,
            "chmod_value": None,
            "destination": "/destination/path",
            "target": "FILE",
        }

        nested_control_data = {
            "id": "control001",
            "block_type": "BASE_CONTROL_BLOCK",
            "control_type": "WHILE",
            "conditions": [
                {"id": "cond002", "block_type": "BASE_CONDITION_BLOCK"},
                {
                    "id": "filecond002",
                    "block_type": "FILE_CONDITION_BLOCK",
                    "condition_type": "FILE",
                    "detail_condition_type": ["FILE_OWNER"],
                    "value": "admin",
                },
            ],
            "body": [
                {
                    "id": "control001",
                    "block_type": "BASE_CONTROL_BLOCK",
                    "control_type": "WHILE",
                    "conditions": [
                        {"id": "cond002", "block_type": "BASE_CONDITION_BLOCK"},
                        {
                            "id": "filecond002",
                            "block_type": "FILE_CONDITION_BLOCK",
                            "condition_type": "FILE",
                            "detail_condition_type": ["FILE_OWNER"],
                            "value": "admin",
                        },
                    ],
                    "body": [
                        {
                            "id": "fileaction001",
                            "block_type": "FILE_ACTION_BLOCK",
                            "action": "COPY",
                            "target_loc": "/source/path",
                            "target_detail": "FILE_NAME",
                            "replace_text": None,
                            "chmod_value": None,
                            "destination": "/destination/path",
                            "target": "FILE",
                        },
                        {"id": "simple002", "block_type": "BASE_CONDITION_BLOCK"},
                    ],
                },
                {
                    "id": "control001",
                    "block_type": "BASE_CONTROL_BLOCK",
                    "control_type": "WHILE",
                    "conditions": [
                        {"id": "cond002", "block_type": "BASE_CONDITION_BLOCK"},
                        {
                            "id": "filecond002",
                            "block_type": "FILE_CONDITION_BLOCK",
                            "condition_type": "FILE",
                            "detail_condition_type": ["FILE_OWNER"],
                            "value": "admin",
                        },
                    ],
                    "body": [
                        {
                            "id": "fileaction001",
                            "block_type": "FILE_ACTION_BLOCK",
                            "action": "COPY",
                            "target_loc": "/source/path",
                            "target_detail": "FILE_NAME",
                            "replace_text": None,
                            "chmod_value": None,
                            "destination": "/destination/path",
                            "target": "FILE",
                        },
                        {
                            "id": "control001",
                            "block_type": "BASE_CONTROL_BLOCK",
                            "control_type": "WHILE",
                            "conditions": [
                                {"id": "cond002", "block_type": "BASE_CONDITION_BLOCK"},
                                {
                                    "id": "filecond002",
                                    "block_type": "FILE_CONDITION_BLOCK",
                                    "condition_type": "FILE",
                                    "detail_condition_type": ["FILE_OWNER"],
                                    "value": "admin",
                                },
                            ],
                            "body": [
                                {
                                    "id": "fileaction001",
                                    "block_type": "FILE_ACTION_BLOCK",
                                    "action": "COPY",
                                    "target_loc": "/source/path",
                                    "target_detail": "FILE_NAME",
                                    "replace_text": None,
                                    "chmod_value": None,
                                    "destination": "/destination/path",
                                    "target": "FILE",
                                },
                                {
                                    "id": "simple002",
                                    "block_type": "BASE_CONDITION_BLOCK",
                                },
                            ],
                        },
                    ],
                },
            ],
        }
        test_cases = {
            # "Condition Block Case": condition_block_data,
            # "File Condition Block Case": file_condition_block_data,
            # "Control Block Case": control_block_data,
            # "base action block case ": action_block,
            "nested control block case": nested_control_data
        }

        # Iterate through each test case
        for test_name, test_data in test_cases.items():
            serializer = GenericSerializer(test_data)
            if serializer.is_valid():
                domain = serializer.to_domain_object()
                print("test_name: ", test_name)
                print(domain)
                print("")
            else:
                print(serializer.errors)
            # Benchmark Custom Serializer
            # custom_time = timeit(use_custom_serializer, number=iterations)

        #     # Append the results
        #     results.append(
        #         {
        #             "Test Case": test_name,
        #             "Custom Serializer Time (s)": custom_time,
        #             "Faster Serializer": "Custom Serializer",  # Only one serializer is used
        #         }
        #     )

        # # Display the results
        # self.stdout.write("\nBenchmark Results:\n")
        # self.stdout.write(
        #     f"{'Test Case':<25} {'Custom Serializer (s)':<25} {'Faster Serializer'}"
        # )
        # for result in results:
        #     self.stdout.write(
        #         f"{result['Test Case']:<25} {result['Custom Serializer Time (s)']:<25.6f} {result['Faster Serializer']}"
        #     )
