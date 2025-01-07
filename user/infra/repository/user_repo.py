from django.db import DatabaseError

from user.domain.user import User as UserVo
from user.infra.models.serializer import UserSerializer
from user.infra.models.user import User
from user.service.repository.i_user_repo import IUserRepo


class UserRepo(IUserRepo):
    def get_user(self, filter: IUserRepo.Filter) -> UserVo | None:
        user = User.object.all()
        if filter.oauth_id and filter.oauth_type:
            user = user.filter(oauth_id=filter.oauth_id, oauth_type=filter.oauth_type)
        if filter.user_id:
            user = user.filter(id=filter.user_id)

        serializer = UserSerializer(user)
        user_dict = serializer.data

        if user_dict:
            return UserVo.from_dict(dto=user_dict)

        return None

    def get_bulk(self):
        pass

    def create(self, user_vo: UserVo) -> UserVo:
        serializer = UserSerializer(data=user_vo.to_dict)

        if serializer.is_valid():
            serializer.save()

            return user_vo.from_dict(serializer.data)
        else:
            raise DatabaseError(serializer.errors)
