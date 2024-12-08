from user.domain.user import OAuthType, OAuthUser
from user.service.oauth.i_oauth_provider import IOAuthProvider


class Kakao(IOAuthProvider):
    def get_oauth_token(self, oauth_code: str) -> str:
        return "sample_token"

    def get_oauth_user(self, access_token: str) -> OAuthUser:
        # 예시임
        return OAuthUser(
            oauth_type=OAuthType.KAKAO,
            id="",
            email="",
            name="",
            mobile_no="",
        )
