# exceptions.py
class ValidationError(Exception):
    pass


class BlockTypeMismatchError(ValidationError):
    """잘못된 블록 타입 사용"""

    def __init__(self, message="블록 타입이 잘못되었습니다."):
        super().__init__(message)


class MissingControlBlockError(ValidationError):
    """Control 블록 없이 Condition 블록이 단독으로 사용된 경우"""

    def __init__(self, message="Control 블록 없이 Condition 블록이 독립적으로 사용될 수 없습니다."):
        super().__init__(message)


class InvalidBlockPositionError(ValidationError):
    """블록이 올바른 위치에 있지 않은 경우"""

    def __init__(self, block_type, expected_position):
        message = f"블록 타입 {block_type}은(는) {expected_position} 위치에 있어야 합니다."
        super().__init__(message)
