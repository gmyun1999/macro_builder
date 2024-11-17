class WorksheetException(Exception):
    """워크시트 관련 기본 예외 클래스."""

    code = "WORKSHEET_ERROR"

    def __init__(self, message: str = "워크시트 관련 오류가 발생했습니다.", detail: dict = {}):
        super().__init__(message)
        self.detail = detail


class FunctionException(Exception):
    """함수 관련 기본 예외 클래스."""

    code = "FUNCTION_ERROR"

    def __init__(self, message: str = "함수 관련 오류가 발생했습니다.", detail: dict = {}):
        super().__init__(message)
        self.detail = detail


class NotLoggedInException(WorksheetException):
    """사용자가 로그인하지 않은 경우 발생하는 예외."""

    code = "NOT_LOGGED_IN"

    def __init__(self, message: str = "로그인을 하지 않으면 저장이 불가능합니다.", detail: dict = {}):
        super().__init__(message, detail)


class WorksheetNotFoundException(WorksheetException):
    """워크시트를 찾을 수 없는 경우 발생하는 예외."""

    code = "WORKSHEET_NOT_FOUND"

    def __init__(
        self, worksheet_id: str, message: str = "해당되는 워크시트가 없습니다.", detail: dict = {}
    ):
        self.worksheet_id = worksheet_id
        super().__init__(f"{message} (ID: {worksheet_id})", detail)


class FunctionNotFoundException(FunctionException):
    """관련 함수 ID가 존재하지 않는 경우 발생하는 예외."""

    code = "FUNCTION_NOT_FOUND"

    def __init__(
        self, function_id: str, message: str = "관련 함수 ID가 존재하지 않습니다.", detail: dict = {}
    ):
        self.function_id = function_id
        super().__init__(f"{message} (Function ID: {function_id})", detail)


class FunctionRecursionException(FunctionException):
    """관련 함수 ID가 현재 FUNCTION에 들어있어서 무한재귀 예외."""

    code = "FUNCTION_RECURSION"

    def __init__(
        self, function_id: str, message: str = "재귀 함수는 허용하지않습니다.", detail: dict = {}
    ):
        self.function_id = function_id
        super().__init__(f"{message} (Function ID: {function_id})", detail)


class FunctionCircularException(FunctionException):
    """관련 함수 ID가 순환참조를 발생시킬때 예외."""

    code = "FUNCTION_CIRCULAR"

    def __init__(
        self, function_id: str, message: str = "관련함수가 순환참조를 발생시킵니다.", detail: dict = {}
    ):
        self.function_id = function_id
        super().__init__(f"{message} (Function ID: {function_id})", detail)


class FunctionHasChildrenException(FunctionException):
    """함수를 삭제할떄 이함수를 참조하는 자식함수들이 있을때 예외"""

    code = "FUNCTION_HAS_CHILDREN"

    def __init__(
        self,
        function_id: str,
        message: str = "관련함수를 참조하는 자식함수들이 있습니다..",
        detail: dict = {},
    ):
        self.function_id = function_id
        super().__init__(f"{message} (Function ID: {function_id})", detail)


class GenerateGuiException(Exception):
    """gui 생성 관련 기본 예외 클래스."""

    code = "GUI_GENERATE_ERROR"

    def __init__(self, message: str = "gui 생성관련 오류가 발생했습니다.", detail: dict = {}):
        super().__init__(message)
        self.detail = detail


class MainBlockEmptyException(GenerateGuiException):
    """함수를 삭제할떄 이함수를 참조하는 자식함수들이 있을때 예외"""

    code = "MAIN_BLOCK_EMPTY"

    def __init__(
        self,
        message: str = "main block은 비어있을수없습니다",
        detail: dict = {},
    ):
        super().__init__(message, detail)


class DownloadLinkNotFoundException(GenerateGuiException):
    """gui 스토리지 link가 오지않았을때 예외"""

    code = "GUI_LINK_NOT_FOUND"

    def __init__(
        self,
        message: str = "gui link가 오지않았음",
        detail: dict = {},
    ):
        super().__init__(message, detail)
