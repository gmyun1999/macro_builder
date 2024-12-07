from abc import ABC, abstractmethod


class IKoLawRepo(ABC):
    @abstractmethod
    def get_org_from_org_name(self, org_name: str) -> str | None:
        pass
