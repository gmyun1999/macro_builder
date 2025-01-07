from datetime import datetime, timedelta

import jwt

from common.service.token.i_token_manager import ITokenManager
from macro_be import settings
from user.domain.user_role import UserRole
from user.domain.user_token import UserTokenExp, UserTokenPayload, UserTokenType


class UserTokenManager(ITokenManager):
    JWT_ALGORITHM = "HS512"
    JWT_SECRET = settings.JWT_SECRET

    def create_admin_access_token(self, admin_id: str) -> str:
        payload = self._create_user_token_payload(
            admin_id=admin_id,
            role=UserRole.ADMIN,
            type=UserTokenType.ACCESS,
            seconds=UserTokenExp.ACCESS_EXP,
        )
        return self._create_user_token(user_payload_vo=payload)

    def create_guest_access_token(self, guest_id: str) -> str:
        payload = self._create_user_token_payload(
            guest_id=guest_id,
            role=UserRole.GUEST,
            type=UserTokenType.REFRESH,
            seconds=UserTokenExp.REFRESH_EXP,
        )
        return self._create_user_token(user_payload_vo=payload)

    def create_admin_refresh_token(self, admin_id: str) -> str:
        payload = self._create_user_token_payload(
            admin_id=admin_id,
            role=UserRole.ADMIN,
            type=UserTokenType.REFRESH,
            seconds=UserTokenExp.REFRESH_EXP,
        )
        return self._create_user_token(user_payload_vo=payload)

    def create_user_access_token(self, user_id: str) -> str:
        payload = self._create_user_token_payload(
            user_id=user_id,
            role=UserRole.USER,
            type=UserTokenType.ACCESS,
            seconds=UserTokenExp.ACCESS_EXP,
        )
        return self._create_user_token(user_payload_vo=payload)

    def create_user_refresh_token(self, user_id: str) -> str:
        payload = self._create_user_token_payload(
            user_id=user_id,
            role=UserRole.USER,
            type=UserTokenType.REFRESH,
            seconds=UserTokenExp.REFRESH_EXP,
        )
        return self._create_user_token(user_payload_vo=payload)

    def _create_user_token_payload(
        self,
        user_id: str | None = None,
        admin_id: str | None = None,
        guest_id: str | None = None,
        role: UserRole = UserRole.USER,
        type: str = UserTokenType.ACCESS,
        seconds: int = UserTokenExp.ACCESS_EXP,
    ) -> UserTokenPayload:
        return UserTokenPayload(
            admin_id=admin_id,
            user_id=user_id,
            guest_id=guest_id,
            role=role,
            type=type,
            exp=int((datetime.now() + timedelta(seconds=seconds)).timestamp()),  # 만료시간
            iat=int(datetime.now().timestamp()),  # 발급시간
        )

    def _create_user_token(self, user_payload_vo: UserTokenPayload) -> str:
        payload = user_payload_vo.to_dict()
        jwt_token = jwt.encode(payload, self.JWT_SECRET, self.JWT_ALGORITHM)

        return jwt_token
