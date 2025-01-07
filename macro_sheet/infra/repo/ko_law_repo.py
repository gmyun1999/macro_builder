from macro_sheet.infra.models import KoOrg
from macro_sheet.service.i_repo.i_ko_law_repo import IKoLawRepo


class KoLawRepo(IKoLawRepo):
    def get_org_from_org_name(self, org_name: str) -> str | None:
        """
        org : 소관부처 코드
        org_name : 소관부처명
        return : org
        """
        try:
            return KoOrg.objects.get(org_name=org_name).org
        except KoOrg.DoesNotExist:
            return None
