from abc import ABCMeta, abstractmethod

from user.domain.user import User as userVo


class IUserRepo(metaclass=ABCMeta):
    class Filter:
        def __init__(
            self,
            user_id: str | None = None,
            oauth_id: str | None = None,
            oauth_type: str | None = None,
        ):
            self.user_id = user_id
            self.oauth_id = oauth_id
            self.oauth_type = oauth_type

    @abstractmethod
    def get_user(self, filter: Filter) -> userVo | None:
        pass

    @abstractmethod
    def create(self, user_vo: userVo) -> userVo:
        pass
