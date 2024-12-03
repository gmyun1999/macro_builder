from datetime import datetime, timedelta

import jwt

from common.infra.token.token import (
    BackendAccessTokenExp,
    BackendAccessTokenPayload,
    BackendAccessTokenType,
)
from common.service.token.i_token_manager import ITokenManager
from macro_be import settings


class BackendAccessToken:
    JWT_ALGORITHM = "HS512"
    JWT_SECRET = settings.JWT_SECRET

    def create_git_action_bankend_access_token(self) -> str:
        payload = self._create_bankend_access_token_payload(
            type=BackendAccessTokenType.ACCESS,
            seconds=BackendAccessTokenExp.ACCESS_EXP,
        )

        return self._create_backend_access_token(backend_access_payload_vo=payload)

    def _create_bankend_access_token_payload(
        self,
        type: str = BackendAccessTokenType.ACCESS,
        seconds: int = BackendAccessTokenExp.ACCESS_EXP,
    ) -> BackendAccessTokenPayload:
        return BackendAccessTokenPayload(
            type=type,
            exp=int((datetime.now() + timedelta(seconds=seconds)).timestamp()),  # 만료시간
            iat=int(datetime.now().timestamp()),  # 발급시간
        )

    def _create_backend_access_token(
        self, backend_access_payload_vo: BackendAccessTokenPayload
    ) -> str:
        payload = backend_access_payload_vo.to_dict()
        jwt_token = jwt.encode(payload, self.JWT_SECRET, self.JWT_ALGORITHM)

        return jwt_token
