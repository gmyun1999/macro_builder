from user.domain.user import OAuthUser
from user.service.oauth.i_oauth_provider import IOAuthProvider


class Kakao(IOAuthProvider):
    def get_oauth_token(self, oauth_code: str) -> str:
        pass

    def get_oauth_user(self, access_token: str) -> OAuthUser:
        pass
