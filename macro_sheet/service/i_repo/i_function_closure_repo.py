from abc import ABC, abstractmethod


class IFunctionClosureRepo(ABC):
    class Filter:
        def __init__(self, parent_id: str | None = None, child_id: str | None = None):
            self.parent_id = parent_id
            self.child_id = child_id

    class Closure:
        def __init__(self, parent_id: str, child_id: str):
            self.parent_id = parent_id
            self.child_id = child_id

    @abstractmethod
    def save(self, closure: Closure) -> None:
        pass

    @abstractmethod
    def delete(self, closure: Closure) -> None:
        pass

    @abstractmethod
    def fetch(self, filter: Filter) -> list[Closure]:
        """
        필터에 맞는 Closure 리스트를 반환합니다.
        """
        pass

    @abstractmethod
    def bulk_save(self, closures: list[Closure]) -> None:
        """
        closures: Closure 객체 리스트
        """
        pass

    @abstractmethod
    def bulk_delete(self, closures: list[Closure]) -> None:
        """
        closures: Closure 객체 리스트
        """
        pass

    @abstractmethod
    def get_all_ancestors(self, root_function_id: str) -> list[str]:
        pass
