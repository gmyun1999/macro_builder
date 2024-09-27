from typing import Dict, Type

from macro_sheet.domain.block.block import Block, BlockType

BLOCK_TYPE_REGISTRY: Dict[str, Type[Block]] = {}


def register_block_type(block_type: BlockType):
    """
    데코레이터를 사용하여 블록 타입을 레지스트리에 등록
    새로운 block_type의 클래스가 생성되면 이거 붙여주기!
    """

    def decorator(cls: Type[Block]):
        BLOCK_TYPE_REGISTRY[block_type.value] = cls
        return cls

    return decorator
