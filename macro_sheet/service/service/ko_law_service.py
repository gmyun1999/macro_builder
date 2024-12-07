from macro_sheet.infra.repo.ko_law_repo import KoLawRepo
from macro_sheet.service.i_repo.i_ko_law_repo import IKoLawRepo


class KoLawService:
    def __init__(self):
        # TODO: DI
        self.ko_law_repo: IKoLawRepo = KoLawRepo()

    def get_org(self, org_name: str) -> str:
        org = self.ko_law_repo.get_org_from_org_name(org_name)

        if org is None:
            raise ValueError("소관부처명이 존재하지 않습니다.")

        return org
