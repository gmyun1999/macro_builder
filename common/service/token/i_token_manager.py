from abc import ABCMeta, abstractmethod


class ITokenManager(metaclass=ABCMeta):
    @abstractmethod
    def create_admin_access_token(self, admin_id: str) -> str:
        pass

    @abstractmethod
    def create_admin_refresh_token(self, admin_id: str) -> str:
        pass

    @abstractmethod
    def create_user_access_token(self, user_id: str) -> str:
        pass

    @abstractmethod
    def create_user_refresh_token(self, user_id: str) -> str:
        pass
