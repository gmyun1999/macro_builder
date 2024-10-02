from abc import ABC, abstractmethod
from typing import Tuple

from macro_sheet.domain.block.action_block.file_action_block import FileActionBlock
from macro_sheet.domain.block.block import Block
from macro_sheet.domain.block.condition_block.file_condition_block import (
    FileConditionBlock,
)
from macro_sheet.domain.block.control_block.control_block import ControlBlock
from macro_sheet.domain.worksheet import Worksheet


class IGuiCodeGeneratorFromBlock(ABC):
    @abstractmethod
    def generate_gui_code(self, block: Block) -> str:
        """
        nested Block의 도메인 객체에 맞는 piece 코드들을 실행시켜 그에맞는
        코드를 반환받고 이러한 코드의 전체적인 조합을 여기서 결합시킨후
        전체 코드를 반환한다.
        """
        pass

    @abstractmethod
    def piece_code_from_file_action(self, block: FileActionBlock) -> str:
        """
        file action 블록의 코드에 맞는 코드를 동적으로 생성해야함
        """
        pass

    @abstractmethod
    def piece_code_from_file_condition(self, block: FileConditionBlock) -> str:
        """
        file condition 블록의 코드에 맞는 코드를 동적으로 생성해야함
        """
        pass

    @abstractmethod
    def piece_code_from_control(self, block: ControlBlock) -> Tuple[str, str]:
        """
        control 블록의 코드에 맞는 코드를 동적으로 생성해야함
        """
        pass
