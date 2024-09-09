import httpx
from macro_be.settings import BASE_URL, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
from user.domain.user import OAuthType, OAuthUser
from user.service.oauth.i_oauth_provider import IOAuthProvider


class Google(IOAuthProvider):
    def get_oauth_token(self, oauth_code: str) -> str:
        res = httpx.request(
            method="POST",
            url="https://oauth2.googleapis.com/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "authorization_code",
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uri": f"{BASE_URL}/user/login/google",
                "code": oauth_code,
            },
        ).json()

        return res["access_token"]

    def get_oauth_user(self, access_token: str) -> OAuthUser:
        res = httpx.request(
            method="GET",
            url="https://www.googleapis.com/oauth2/v2/userinfo",
            headers={
                "Authorization": f"Bearer {access_token}",
            },
        ).json()

        user = OAuthUser(id=res["id"], oauth_type=OAuthType.GOOGLE)
        user.name = res.get("name", None)
        user.email = res.get("email")

        return user
