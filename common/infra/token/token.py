from dataclasses import dataclass
from enum import IntEnum, StrEnum

from common.domain import Domain


class BackendAccessTokenType(StrEnum):
    ACCESS = "ACCESS"


class BackendAccessTokenExp(IntEnum):
    ACCESS_EXP = 5_184_000_000


@dataclass
class BackendAccessTokenPayload(Domain):
    FIELD_TYPE = "type"
    FIELD_EXP = "exp"
    FIELD_IAT = "iat"

    type: str
    exp: int  # 만료시간
    iat: int  # 발급시간
