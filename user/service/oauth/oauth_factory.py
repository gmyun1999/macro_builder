from user.domain.user import OAuthType
from user.infra.oauth.apple import Apple
from user.infra.oauth.google import Google
from user.infra.oauth.kakao import Kakao
from user.service.oauth.i_oauth_provider import IOAuthProvider


class OauthFactory:
    def create(self, oauth_type: OAuthType) -> IOAuthProvider:
        if oauth_type == OAuthType.APPLE:
            return Apple()
        if oauth_type == OAuthType.GOOGLE:
            return Google()
        if oauth_type == OAuthType.KAKAO:
            return Kakao()
