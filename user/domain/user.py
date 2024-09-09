from dataclasses import dataclass
from enum import StrEnum

from common.domain import Domain


class OAuthType(StrEnum):
    KAKAO = "kakao"
    GOOGLE = "google"
    APPLE = "apple"


@dataclass
class User(Domain):
    """
    유저: OAuth 로그인만 가능
    """

    FIELD_ID = "id"
    FIELD_NAME = "name"
    FIELD_EMAIL = "email"
    FIELD_MOBILE_NO = "mobile_no"
    FIELD_OAUTH_TYPE = "oauth_type"
    FIELD_OAUTH_ID = "oauth_id"
    FIELD_TOS_AGREED = "tos_agreed"
    FIELD_CREATED_AT = "created_at"
    FIELD_UPDATED_AT = "updated_at"

    id: str
    name: str | None
    email: str | None
    mobile_no: str | None
    oauth_type: OAuthType
    oauth_id: str
    tos_agreed: bool
    created_at: str
    updated_at: str


@dataclass
class OAuthUser:
    id: str  # id는 uuid가 아니라 Oauth server가 넘겨준 id 를 의미함
    oauth_type: OAuthType
    name: str | None = None
    email: str | None = None
    mobile_no: str | None = None
