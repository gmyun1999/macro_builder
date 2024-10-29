from abc import ABC, abstractmethod
from typing import Tuple

from macro_sheet.domain.block.action_block.action_block import ActionBlock
from macro_sheet.domain.block.action_block.file_action_block import FileActionBlock
from macro_sheet.domain.block.block import Block
from macro_sheet.domain.block.condition_block.condition_block import ConditionBlock
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
    def process_action_block(self, block: ActionBlock) -> str:
        """ActionBlock의 서브 클래스를 확인하여 적절한 GUI 코드 생성 메소드 호출"""
        pass

    @abstractmethod
    def process_condition_block(self, block: ConditionBlock) -> str:
        """ConditionBlock의 서브 클래스를 확인하여 적절한 GUI 코드 생성 메소드 호출"""
        pass

    @abstractmethod
    def process_control_block(self, block: ControlBlock) -> str:
        """ControlBlock의 코드를 생성하고 body와 conditions를 재귀적으로 처리"""
        pass
