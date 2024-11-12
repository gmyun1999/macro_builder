class WorksheetException(Exception):
    """워크시트 관련 기본 예외 클래스."""

    code = "WORKSHEET_ERROR"

    def __init__(self, message: str = "워크시트 관련 오류가 발생했습니다."):
        super().__init__(message)


class NotLoggedInException(WorksheetException):
    """사용자가 로그인하지 않은 경우 발생하는 예외."""

    code = "NOT_LOGGED_IN"

    def __init__(self, message: str = "로그인을 하지 않으면 저장이 불가능합니다."):
        super().__init__(message)


class WorksheetNotFoundException(WorksheetException):
    """워크시트를 찾을 수 없는 경우 발생하는 예외."""

    code = "WORKSHEET_NOT_FOUND"

    def __init__(self, worksheet_id: str, message: str = "해당되는 워크시트가 없습니다."):
        self.worksheet_id = worksheet_id
        super().__init__(f"{message} (ID: {worksheet_id})")


class FunctionNotFoundException(WorksheetException):
    """관련 함수 ID가 존재하지 않는 경우 발생하는 예외."""

    code = "FUNCTION_NOT_FOUND"

    def __init__(self, function_id: str, message: str = "관련 함수 ID가 존재하지 않습니다."):
        self.function_id = function_id
        super().__init__(f"{message} (Function ID: {function_id})")
