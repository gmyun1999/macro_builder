class PagingException(Exception):
    """페이징 관련 예외 클래스."""

    code = "UNKNOWN_PAGING_ERROR"


class InvalidPagingParameterException(PagingException):
    """유효하지 않은 페이징 파라미터가 전달된 경우 발생하는 예외."""

    code = "INVALID_PAGING_PARAMETER"

    def __init__(self, message: str = "유효하지 않은 페이징 파라미터가 전달되었습니다."):
        super().__init__(message)
