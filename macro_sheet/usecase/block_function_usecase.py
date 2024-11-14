from common.service.paging import Paginator
from macro_sheet.domain.Function.block_function import BlockFunction
from macro_sheet.service.exception.exceptions import (
    FunctionCircularException,
    FunctionHasChildrenException,
    FunctionNotFoundException,
    FunctionRecursionException,
)
from macro_sheet.service.service.block_function_service import BlockFunctionService


class BlockFunctionUseCase:
    def __init__(self) -> None:
        self.block_function_service = BlockFunctionService()

    def fetch_process(self):
        pass

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
        self, block_function: BlockFunction, related_function_ids: list[str] | None
    ) -> BlockFunction:
        """기존의 블럭함수를 수정하는"""
        if related_function_ids is not None:
            if not self.block_function_service.check_is_exist_id(
                function_id=block_function.id
            ):
                raise FunctionNotFoundException(block_function.id)

            if self.block_function_service.check_recursion(
                function_id=block_function.id, related_function_ids=related_function_ids
            ):
                raise FunctionRecursionException(block_function.id)

            if self.block_function_service.check_circular(
                target_function_id=block_function.id,
                related_function_ids=related_function_ids,
            ):
                raise FunctionCircularException(block_function.id)

        return self.block_function_service.update_block_function_with_closure_function(
            block_function_obj=block_function,
            new_parent_function_ids=related_function_ids,
        )

    def create_process(
        self, block_function: BlockFunction, related_function_ids: list[str] | None
    ) -> BlockFunction:
        """
        블럭함수를 새로 생성하는
        - 순환 참조가 발생하는지 체크해야함. - create에서는 발생할수가없음
        - 재귀가 있는지 체크해야함 - create 에서는 발생할수가없음
        - reference block 이 있다면 존재하는지를 체크해야함.
        """
        if related_function_ids is not None:
            if not self.block_function_service.check_is_exist_id(
                function_id=block_function.id
            ):
                raise FunctionNotFoundException(block_function.id)

        return self.block_function_service.create_block_function_with_closure_function(
            block_function_obj=block_function, parent_function_ids=related_function_ids
        )

    def delete_process(self, block_function: BlockFunction) -> bool:
        """
        service 의 delete_block_function_with_closure_function 그대로 쓰면될듯?
        """
        return self.block_function_service.delete_block_function_with_closure_function(
            function_id=block_function.id
        )

    def safety_delete_process(self, block_function: BlockFunction) -> bool:
        """
        has child function이 있다면 삭제하지말고 예외 발생시킴.
        없으면 삭제 시도후 성공여부 반환
        """
        children = self.block_function_service.get_child_function_ids(
            function_id=block_function.id
        )
        if children:
            detail = {"children": children}
            raise FunctionHasChildrenException(
                function_id=block_function.id, detail=detail
            )

        return self.block_function_service.delete_block_function_with_closure_function(
            function_id=block_function.id
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
