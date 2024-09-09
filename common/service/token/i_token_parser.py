from abc import ABCMeta, abstractmethod
from typing import Any


class ITokenParser(metaclass=ABCMeta):
    @abstractmethod
    def decode_token(self, token: str) -> dict[str, Any]:
        """
        토큰을 넣으면 페이로드를 반환
        return: payload dict
        """
        pass

    @abstractmethod
    def check_token(
        self, token: str, allowed_roles: list[str], validate_type: str
    ) -> tuple[Any | None, str]:
        """
        params: 토큰, 역할, access | refresh
        return: tuple[TokenPayLoad_Vo | None, msg]
        """
        pass

    @abstractmethod
    def get_token(self, http_header: Any) -> str:
        """
        http_header로부터 token을 return 함
        """
