from typing import Any

import jwt
from django.http.request import HttpHeaders

from common import response_msg
from common.constant import RequestHeader
from common.infra.token.token import BackendAccessTokenPayload
from common.service.token.i_token_parser import ITokenParser
from macro_be.settings import JWT_SECRET


class BackendAccessToken(ITokenParser):
    JWT_ALGORITHM = "HS512"
    JWT_SECRET = JWT_SECRET

    def _validate_token(
        self, token: str, validate_type: str
    ) -> tuple[BackendAccessTokenPayload | None, str]:
        if not token:
            return None, response_msg.TokenMessage.NOT_FOUND.value
        try:
            payload = self.decode_token(token)

            if payload[BackendAccessTokenPayload.FIELD_TYPE] != validate_type:
                return None, response_msg.TokenMessage.WRONG_TYPE.value

            token_payload_vo = BackendAccessTokenPayload.from_dict(payload)
            return token_payload_vo, response_msg.TokenMessage.VALID.value

        except jwt.ExpiredSignatureError:
            return None, response_msg.TokenMessage.EXPIRED.value

    def check_token(
        self, token: str, allowed_roles: list[str], validate_type: str
    ) -> tuple[BackendAccessTokenPayload | None, str]:
        """
        allowed_roles에 빈리스트 넘겨주면됩니다.
        """
        allowed_roles = allowed_roles
        payload_vo, msg = self._validate_token(token=token, validate_type=validate_type)

        if not payload_vo:
            print(f"Invalid Token: {msg}")
            return None, msg

        return payload_vo, msg

    def decode_token(self, token: str) -> dict[str, Any]:
        return jwt.decode(token, self.JWT_SECRET, algorithms=[self.JWT_ALGORITHM])

    def get_token(self, http_header: HttpHeaders) -> str:
        authorization = http_header.get(RequestHeader.HEADER_AUTHORIZATION, "")
        return authorization.replace(RequestHeader.HEADER_PREFIX_BEARER, "")
