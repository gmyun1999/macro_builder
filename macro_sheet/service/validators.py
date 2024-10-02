from macro_sheet.domain.block.block import Block
from macro_sheet.domain.block.condition_block.condition_block import ConditionBlock
from macro_sheet.domain.block.control_block.control_block import ControlBlock
from macro_sheet.domain.worksheet import Worksheet
from macro_sheet.service.exceptions import (
    BlockTypeMismatchError,
    InvalidBlockPositionError,
    MissingControlBlockError,
)


class SyntaxValidator:
    """
    ControlBlock(id='control001', block_type=<BlockType.BASE_CONTROL_BLOCK: 'BASE_CONTROL_BLOCK'>,
    control_type=<ControlType.WHILE: 'WHILE'>, conditions=[ConditionBlock(id='cond002',
    block_type=<BlockType.BASE_CONDITION_BLOCK: 'BASE_CONDITION_BLOCK'>),
    FileConditionBlock(id='filecond002', block_type=<BlockType.FILE_CONDITION_BLOCK: 'FILE_CONDITION_BLOCK'>,
    condition_type=<ConditionType.FILE: 'FILE'>, detail_condition_type=[<FileConditionType.FILE_OWNER: 'FILE_OWNER'>],
    value='admin')], body=[ControlBlock(id='control001', block_type=<BlockType.BASE_CONTROL_BLOCK: 'BASE_CONTROL_BLOCK'>,
    control_type=<ControlType.WHILE: 'WHILE'>, conditions=[ConditionBlock(id='cond002',
    block_type=<BlockType.BASE_CONDITION_BLOCK: 'BASE_CONDITION_BLOCK'>),
    FileConditionBlock(id='filecond002', block_type=<BlockType.FILE_CONDITION_BLOCK: 'FILE_CONDITION_BLOCK'>,
    condition_type=<ConditionType.FILE: 'FILE'>, detail_condition_type=[<FileConditionType.FILE_OWNER: 'FILE_OWNER'>],
    value='admin')], body=[FileActionBlock(id='fileaction001', block_type=<BlockType.FILE_ACTION_BLOCK: 'FILE_ACTION_BLOCK'>,
    action=<FileActionType.COPY: 'COPY'>, target_loc='/source/path', target_detail=<FileTargetDetail.FILE_NAME: 'FILE_NAME'>,
    replace_text=None, chmod_value=None, destination='/destination/path', target=<TargetType.FILE: 'FILE'>),
    ConditionBlock(id='simple002', block_type=<BlockType.BASE_CONDITION_BLOCK: 'BASE_CONDITION_BLOCK'>)]),
    ControlBlock(id='control001', block_type=<BlockType.BASE_CONTROL_BLOCK: 'BASE_CONTROL_BLOCK'>,
    control_type=<ControlType.WHILE: 'WHILE'>,
    conditions=[ConditionBlock(id='cond002',
    block_type=<BlockType.BASE_CONDITION_BLOCK: 'BASE_CONDITION_BLOCK'>),
    FileConditionBlock(id='filecond002',
    block_type=<BlockType.FILE_CONDITION_BLOCK: 'FILE_CONDITION_BLOCK'>,
    condition_type=<ConditionType.FILE: 'FILE'>,
    detail_condition_type=[<FileConditionType.FILE_OWNER: 'FILE_OWNER'>], value='admin')],
    body=[FileActionBlock(id='fileaction001', block_type=<BlockType.FILE_ACTION_BLOCK: 'FILE_ACTION_BLOCK'>,
    action=<FileActionType.COPY: 'COPY'>, target_loc='/source/path', target_detail=<FileTargetDetail.FILE_NAME: 'FILE_NAME'>,
    replace_text=None, chmod_value=None, destination='/destination/path', target=<TargetType.FILE: 'FILE'>),
    ControlBlock(id='control001', block_type=<BlockType.BASE_CONTROL_BLOCK: 'BASE_CONTROL_BLOCK'>,
    control_type=<ControlType.WHILE: 'WHILE'>, conditions=[ConditionBlock(id='cond002',
    block_type=<BlockType.BASE_CONDITION_BLOCK: 'BASE_CONDITION_BLOCK'>),
    FileConditionBlock(id='filecond002', block_type=<BlockType.FILE_CONDITION_BLOCK: 'FILE_CONDITION_BLOCK'>,
    condition_type=<ConditionType.FILE: 'FILE'>, detail_condition_type=[<FileConditionType.FILE_OWNER: 'FILE_OWNER'>],
    value='admin')], body=[FileActionBlock(id='fileaction001', block_type=<BlockType.FILE_ACTION_BLOCK: 'FILE_ACTION_BLOCK'>,
    action=<FileActionType.COPY: 'COPY'>, target_loc='/source/path', target_detail=<FileTargetDetail.FILE_NAME: 'FILE_NAME'>,
    replace_text=None, chmod_value=None, destination='/destination/path', target=<TargetType.FILE: 'FILE'>),
    ConditionBlock(id='simple002', block_type=<BlockType.BASE_CONDITION_BLOCK: 'BASE_CONDITION_BLOCK'>)])])])
       위 예시는 dict로 보낸걸 도메인 객체로 변경해준 실제값임. 다음과같은 도메인 객체를 넘겨줄때 문법적으로 블록이 알맞은 위치에 들어있는지를
       판단해줘야함.
       예를들어서 받은 도메인 객체가
       FileConditionBlock 하나만 존재한다고 가정해보자.
       condition 블록은 '조건' 그 자체이므로 독립적으로 존재할수없음
       따라서 control 블록의 condition 부분에 들어가던가 해야함.
       이경우 문법적으로 에러임.
       -> 이러한 경우들을  validator에서 걸러야함.
       밑의 함수들은 샘플 코드입니다. 알아서 로직에 맞게 수정하시면됩니다.

    """

    def validate(self, worksheet: Worksheet):
        for block in worksheet.blocks:
            if isinstance(block, ConditionBlock):
                self._validate_condition_block(block)
            elif isinstance(block, ControlBlock):
                self._validate_control_block(block)
            else:
                # 블록 타입이 올바르지 않을 때 예외 발생
                raise BlockTypeMismatchError()

    def _validate_condition_block(self, block: ConditionBlock):
        # ConditionBlock이 ControlBlock 없이 독립적으로 있는지 확인

        if not self._is_within_control_block(block):
            raise MissingControlBlockError()

    def _validate_control_block(self, block: ControlBlock):
        # ControlBlock의 내부 구조를 검증
        for condition in block.conditions:
            if not isinstance(condition, ConditionBlock):
                raise InvalidBlockPositionError()

    def _is_within_control_block(self, block: ConditionBlock) -> bool:
        # ConditionBlock이 ControlBlock 안에 있는지 확인하는 로직

        return isinstance(block.parent, ControlBlock)
