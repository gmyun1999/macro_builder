from dataclasses import dataclass

import arrow
from django.http import HttpRequest, JsonResponse
from pydantic import BaseModel, Field
from rest_framework import status
from rest_framework.views import APIView
from ulid import ULID

from common.interface.validators import validate_query_params
from user.domain.user import OAuthType, User
from user.domain.user_role import UserRole
from user.domain.user_token import UserTokenPayload, UserTokenType
from user.interface.validator.user_token_validator import validate_token
from user.service.oauth.i_oauth_provider import IOAuthProvider
from user.service.oauth.oauth_factory import OauthFactory
from user.service.user_service import UserService


class OAuthLoginView(APIView):
    @dataclass
    class AuthCode(BaseModel):
        code: str = Field(min_length=32)

    def __init__(self):
        self.oauth_factory = OauthFactory()
        self.user_service = UserService()

    @validate_query_params(AuthCode)
    def get(self, auth_server: str, params: AuthCode):
        auth_server = OAuthType(auth_server)
        oauth_provider_vo: IOAuthProvider = self.oauth_factory.create(auth_server)
        token = oauth_provider_vo.get_oauth_token(oauth_code=params.code)
        oauth_user_vo = oauth_provider_vo.get_oauth_user(access_token=token)

        user = self.user_service.get_user_from_oauth_user(oauth_user=oauth_user_vo)

        if user is None:
            now = arrow.now().isoformat()
            user = self.user_service.create_user(
                User(
                    id=ULID().generate(),
                    name=oauth_user_vo.name,
                    email=oauth_user_vo.email,
                    mobile_no=oauth_user_vo.mobile_no,
                    oauth_type=auth_server,
                    oauth_id=oauth_user_vo.id,
                    tos_agreed=False,
                    created_at=now,
                    updated_at=now,
                )
            )

        token_dict = self.user_service.create_user_token(user_id=user.id)
        return JsonResponse(status=status.HTTP_200_OK, data=token_dict)


class UserView(APIView):
    pass


class RefreshTokenView(APIView):
    def __init__(self):
        self.user_service = UserService()

    @validate_token(
        roles=[UserRole.USER, UserRole.ADMIN], validate_type=UserTokenType.REFRESH
    )
    def get(
        self,
        request: HttpRequest,
        token_payload: UserTokenPayload,
    ):
        if token_payload.admin_id is not None:
            user_id = token_payload.admin_id
        elif token_payload.user_id is not None:
            user_id = token_payload.user_id

        token: dict = self.user_service.create_access_token(user_id=user_id)

        return JsonResponse(status=status.HTTP_200_OK, data=token)
