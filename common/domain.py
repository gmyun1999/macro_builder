import json
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any, Generic, Type, TypeVar

from arrow import Arrow
from dacite import Config, from_dict

from common.utils.base import remove_none


@dataclass
class Domain:
    @classmethod
    def from_dict(cls: Type, dto: dict[str, Any]):  # 객체로 변환
        return from_dict(
            data_class=cls,
            data=dto,
            config=Config(cast=[Enum, Arrow]),
        )

    def to_dict(self, excludes: list[str] = []) -> dict[str, Any]:  # dict로 변환
        dto = remove_none(json.dumps(asdict(self), default=str))
        if excludes:
            return {key: value for key, value in dto.items() if key not in excludes}
        else:
            return dto


T = TypeVar("T")


@dataclass
class PagedResult(Generic[T]):
    items: list[T]
    total_items: int
    total_pages: int
    current_page: int
    page_size: int
    has_previous: bool
    has_next: bool
