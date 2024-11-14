import uuid

from common.service.paging import Paginator
from macro_sheet.domain.block.block import Block
from macro_sheet.domain.Function.block_function import BlockFunction
from macro_sheet.service.exception.exceptions import (
    FunctionCircularException,
    FunctionHasChildrenException,
    FunctionNotFoundException,
    FunctionRecursionException,
)
from macro_sheet.service.service.block_function_service import BlockFunctionService
from macro_sheet.service.service.block_service import BlockService


class BlockFunctionUseCase:
    def __init__(self) -> None:
        self.block_function_service = BlockFunctionService()
        self.block_service = BlockService()

    def fetch_process(self, function_id: str) -> BlockFunction:
        """
        사용자가 만들었던 block function 불러올 때
        """
        result = self.block_function_service.fetch_function_by_id(
            function_id=function_id
        )
        if not result:
            raise FunctionNotFoundException(function_id)

        return result

    def bulk_fetch_process(self, owner_id: str, page: int = 1, page_size: int = 10):
        """
        사용자가 만든 모든 block functions를 불러올 때
        """

        functions = self.block_function_service.fetch_function_by_owner_id(
            owner_id=owner_id
        )
        paged_result = Paginator.paginate(
            items=functions, page=page, page_size=page_size
        )
        return paged_result

    def update_process(
        self,
        function_id: str,
        owner_id: str,
        name: str,
        raw_blocks: list,
        blocks: list[Block],
    ) -> BlockFunction:
        """기존의 블럭함수를 수정하는"""

        related_function_ids = []
        related_function_ids_set = set()
        # TODO: function_id 만 알면 쓸수있는데, permission을 걸어채워야할듯.

        for block in blocks:
            for func in self.block_service.find_reference_blocks_in_block(block):
                reference_id = func["reference_id"]
                if not self.block_function_service.check_is_exist_id(
                    function_id=reference_id
                ):
                    raise FunctionNotFoundException(reference_id)
                related_function_ids_set.add(reference_id)

        related_function_ids = list(related_function_ids_set)

        block_function = BlockFunction(
            id=function_id,
            owner_id=owner_id,
            name=name,
            blocks=blocks,
            raw_blocks=raw_blocks,
        )

        if self.block_function_service.check_recursion(
            function_id=function_id, related_function_ids=related_function_ids
        ):
            raise FunctionRecursionException(function_id)

        if self.block_function_service.check_circular(
            target_function_id=function_id,
            related_function_ids=related_function_ids,
        ):
            raise FunctionCircularException(function_id)

        return self.block_function_service.update_block_function_with_closure_function(
            block_function_obj=block_function,
            new_parent_function_ids=related_function_ids,
        )

    def create_process(
        self, owner_id: str, name: str, raw_blocks: list, blocks: list[Block]
    ) -> BlockFunction:
        """
        블럭함수를 새로 생성하는
        - 순환 참조가 발생하는지 체크해야함. - create에서는 발생할수가없음
        - 재귀가 있는지 체크해야함 - create 에서는 발생할수가없음
        - reference block 이 있다면 존재하는지를 체크해야함.
        """
        # TODO: function_id 만 알면 쓸수있는데, permission을 걸어채워야할듯.
        related_function_ids = []
        related_function_ids_set = set()

        for block in blocks:
            for func in self.block_service.find_reference_blocks_in_block(block):
                reference_id = func["reference_id"]
                if not self.block_function_service.check_is_exist_id(
                    function_id=reference_id
                ):
                    raise FunctionNotFoundException(reference_id)
                related_function_ids_set.add(reference_id)

        related_function_ids = list(related_function_ids_set)

        block_function = BlockFunction(
            id=str(uuid.uuid4()),
            owner_id=owner_id,
            name=name,
            blocks=blocks,
            raw_blocks=raw_blocks,
        )

        return self.block_function_service.create_block_function_with_closure_function(
            block_function_obj=block_function, parent_function_ids=related_function_ids
        )

    def delete_process(self, function_id: str) -> bool:
        """
        service 의 delete_block_function_with_closure_function 그대로 쓰면될듯?
        """
        return self.block_function_service.delete_block_function_with_closure_function(
            function_id=function_id
        )

    def safety_delete_process(self, function_id: str) -> bool:
        """
        has child function이 있다면 삭제하지말고 예외 발생시킴.
        없으면 삭제 시도후 성공여부 반환
        """
        children = self.block_function_service.get_child_function_ids(
            function_id=function_id
        )
        if children:
            detail = {"children": children}
            raise FunctionHasChildrenException(function_id=function_id, detail=detail)

        return self.block_function_service.delete_block_function_with_closure_function(
            function_id=function_id
        )

    def check_has_child_function(self, block_function: BlockFunction) -> bool:
        """
        function 이 삭제될때 이를 참조하고있는 child function이 있는지 체크하고
        사용자에게 삭제될수있음을 알려주는 용도
        """
        has_child = self.block_function_service.get_child_function_ids(
            function_id=block_function.id
        )
        if has_child:
            return True

        return False

    def validate_function(self, blocks: list[Block]) -> list[str]:
        """
        일단 현재는 존재하는 reference block id 인지를 확인한다.
        """
        not_exist_function_id: set[str] = set()
        # TODO: function_id 만 알면 쓸수있는데, permission을 걸어채워야할듯.

        for block in blocks:
            for func in self.block_service.find_reference_blocks_in_block(block):
                reference_id = func["reference_id"]

                is_exist = self.block_function_service.check_is_exist_id(
                    function_id=reference_id
                )
                if not is_exist:
                    not_exist_function_id.add(reference_id)

        return list(not_exist_function_id)
