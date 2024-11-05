from abc import ABC, abstractmethod

from macro_sheet.domain.Function.block_function import BlockFunction as BlockFunctionVo


class IBlockFunctionRepo(ABC):
    class Filter:
        def __init__(self, id, owner_id):
            self.id = id
            self.owner_id = owner_id

    @abstractmethod
    def fetch_function(self, filter: Filter) -> list[BlockFunctionVo]:
        """
        filter 조건에 맞는 data 모두 fetch
        """
        pass

    @abstractmethod
    def create_function(self, block_function_obj: BlockFunctionVo) -> BlockFunctionVo:
        """
        function 1개 생성
        """
        pass

    @abstractmethod
    def update_function(self, block_function_obj: BlockFunctionVo) -> BlockFunctionVo:
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
