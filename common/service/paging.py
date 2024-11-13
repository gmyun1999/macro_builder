from typing import Generic, TypeVar

from common.domain import PagedResult
from common.service.token.exception import InvalidPagingParameterException

T = TypeVar("T")


class Paginator(Generic[T]):
    MAX_PAGE_SIZE = 100

    @staticmethod
    def paginate(items: list[T], page: int = 1, page_size: int = 10) -> PagedResult[T]:
        if page < 1 or page_size < 1:
            raise InvalidPagingParameterException("페이지 번호와 페이지 크기는 1 이상이어야 합니다.")

        if page_size > Paginator.MAX_PAGE_SIZE:
            raise InvalidPagingParameterException(
                f"페이지 크기는 최대 {Paginator.MAX_PAGE_SIZE}까지 가능합니다."
            )

        total_items = len(items)
        total_pages = (total_items + page_size - 1) // page_size if page_size > 0 else 0

        if page > total_pages and total_pages != 0:
            raise InvalidPagingParameterException("페이지 번호가 총 페이지 수를 초과합니다.")

        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        paged_items = items[start_index:end_index]

        return PagedResult(
            items=paged_items,
            total_items=total_items,
            total_pages=total_pages,
            current_page=page,
            page_size=page_size,
            has_previous=(page > 1),
            has_next=(page < total_pages),
        )
