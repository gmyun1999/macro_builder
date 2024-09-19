from abc import ABC, abstractmethod

from macro_sheet.domain.block.block import Block
from macro_sheet.domain.worksheet import Worksheet


class IWorkSheetCodeGenerator(ABC):
    @abstractmethod
    def generate_workflow_code(self, workflow: Worksheet) -> str:
        pass


class IFlowSheetCodeGenerator(ABC):
    @abstractmethod
    def generate_workflow_code(self, workflow: Worksheet) -> str:
        pass


class IBlockCodeGenerator(ABC):
    @abstractmethod
    def generate_block_code(self, block: Block) -> str:
        pass
