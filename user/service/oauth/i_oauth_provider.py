from abc import ABCMeta, abstractmethod

from user.domain.user import OAuthUser


class IOAuthProvider(metaclass=ABCMeta):
    @abstractmethod
    def get_oauth_token(self, oauth_code: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_oauth_user(self, access_token: str) -> OAuthUser:
        raise NotImplementedError
