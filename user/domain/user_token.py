from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import IntEnum, StrEnum

from common.domain import Domain


class UserTokenType(StrEnum):
    ACCESS = "ACCESS"
    REFRESH = "REFRESH"


class UserTokenExp(IntEnum):
    ACCESS_EXP = 86_400  # 24시간
    REFRESH_EXP = 5_184_000  # 2달


@dataclass
class UserTokenPayload(Domain):
    admin_id: str | None
    user_id: str | None
    type: str
    role: str
    exp: int  # 만료시간
    iat: int  # 발급시간
