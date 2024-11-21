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

APPEND_COMPONENTS = {
    "schemas": {
        "LoopBlock": {
            "type": "object",
            "properties": {
                LoopBlock.FIELD_ITER_CNT: {"type": "string", "example": "5"},
                LoopBlock.FIELD_BODY: {
                    "type": "array",
                    "items": {"$ref": "#/components/schemas/Block"},
                },
                Block.FIELD_BLOCK_TYPE: {
                    "type": "string",
                    "const": BlockType.BASE_LOOP_BLOCK.value,
                },
            },
            "example": {
                "iter_cnt": "5",
                "body": [{}, {}],
                "block_type": "BASE_LOOP_BLOCK",
            },
        },
        "MainBlock": {
            "type": "object",
            "properties": {
                MainBlock.FIELD_BODY: {
                    "type": "array",
                    "items": {"$ref": "#/components/schemas/Block"},
                },
                Block.FIELD_BLOCK_TYPE: {
                    "type": "string",
                    "const": BlockType.MAIN_BLOCK.value,
                },
            },
            "example": {"body": [{}, {}], "block_type": "MAIN_BLOCK"},
        },
        "ReferenceBlock": {
            "type": "object",
            "properties": {
                ReferenceBlock.FIELD_REFERENCE_ID: {
                    "type": "string",
                    "example": "function123",
                },
                ReferenceBlock.FIELD_REFERENCE_FUNCTION_NAME: {
                    "type": "string",
                    "default": "UnKnown",
                    "example": "my_function",
                },
                Block.FIELD_BLOCK_TYPE: {
                    "type": "string",
                    "const": BlockType.REFERENCE_BLOCK.value,
                },
            },
            "example": {
                "reference_id": "function123",
                "reference_function_name": "my_function",
                "block_type": "REFERENCE_BLOCK",
            },
        },
        "FileSystemBlock": {
            "type": "object",
            "properties": {
                FileSystemBlock.FIELD_TARGET: {
                    "type": "string",
                    "enum": [e.value for e in FileSystemType],
                    "example": FileSystemType.FILE.value,
                },
                FileSystemBlock.FIELD_ACTION: {
                    "type": "string",
                    "enum": [e.value for e in FileSystemAction],
                    "example": FileSystemAction.COPY.value,
                },
                FileSystemBlock.FIELD_LOC: {
                    "type": "string",
                    "example": "/path/to/source",
                },
                FileSystemBlock.FIELD_CONDITION: {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            key.value: {"type": "string", "example": "example_value"}
                            for key in FileConditionDetail
                        },
                    },
                },
                FileSystemBlock.FIELD_DESTINATION: {
                    "type": "string",
                    "nullable": True,
                    "example": "/path/to/destination",
                },
                FileSystemBlock.FIELD_RENAME: {
                    "type": "string",
                    "nullable": True,
                    "example": "new_name",
                },
                Block.FIELD_BLOCK_TYPE: {
                    "type": "string",
                    "const": BlockType.FILE_SYSTEM_BLOCK.value,
                },
            },
            "example": {
                "target": "FILE",
                "action": "COPY",
                "loc": "/path/to/source",
                "condition": [],
                "destination": "/path/to/destination",
                "rename": None,
                "block_type": "FILE_SYSTEM_BLOCK",
            },
        },
        "Block": {
            "type": "object",
            "properties": {
                "target": {"type": "string", "example": "example_target"},
                Block.FIELD_BLOCK_TYPE: {
                    "type": "string",
                    "example": BlockType.BASE_BLOCK.value,
                },
            },
        },
    }
}
