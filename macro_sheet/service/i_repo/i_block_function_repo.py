from abc import ABC, abstractmethod

from macro_sheet.domain.Function.block_function import BlockFunction as BlockFunctionVo


class IBlockFunctionRepo(ABC):
    class Filter:
        def __init__(
            self,
            id: str | None = None,
            owner_id: str | None = None,
            parent_id: str | None = None,  # parent_id 에 해당되는 function들을 모두 fetch
            child_id: str | None = None,  # child_id 에 해당되는 function들을 모두 fetch
        ):
            self.id = id
            self.owner_id = owner_id
            self.parent_id = parent_id
            self.child_id = child_id

    @abstractmethod
    def fetch_function(self, filter: Filter) -> list[BlockFunctionVo]:
        """
        filter 조건에 맞는 data 모두 fetch
        """
        pass

    @abstractmethod
    def create_function(
        self, block_function_obj: BlockFunctionVo, parent_function_ids: list[str] | None
    ) -> BlockFunctionVo:
        """
        function 1개 생성
        """
        pass

    @abstractmethod
    def update_function(
        self, block_function_obj: BlockFunctionVo, new_parent_function_ids: list[str]
    ) -> BlockFunctionVo:
        """
        function 1개 update
        """
        pass

    @abstractmethod
    def delete_function(self, function_id: str) -> bool:
        """
        function 삭제
        """
        pass

    @abstractmethod
    def get_all_ancestors(self, root_function_id: str) -> list[str]:
        pass
