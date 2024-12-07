import uuid

import httpx
from django.db import transaction

from .models import KoLawList


class KoLawApiServer:
    def __init__(self, oc: str):  # 사용자 id
        self.oc = oc
        self.default_domain = "https://www.law.go.kr"
        self.domain = (
            f"{self.default_domain}/DRF/lawSearch.do?OC={self.oc}&target=law&type=json"
        )

    class Filter:
        def __init__(
            self,
            page: int = 1,
            search: int = 1,
            display: int = 100,  # 한 페이지에 보여줄 데이터 수
            query: str | None = None,
            efYd: str | None = None,  # 시행일자 범위 예: "20090101~20090130"
            org: str | None = None,  # 소관부처
        ):
            self.page = page
            self.query = query
            self.efYd = efYd
            self.org = org
            self.search = search
            self.display = display

        def set_page(self, page: int):
            self.page = page
            return self

        def set_display(self, display: int):
            self.display = display
            return self

    def auth_fetch_law_list_data(self, filter: Filter) -> list[dict]:
        """
        자동으로 page가 end 가될떄까지 모든 데이터를 다가져옴
        """
        total_law_data: list[dict] = []
        filter.set_page(1)
        filter.set_display(100)

        while True:
            total_item, fetched_data = self.fetch_law_list_data(filter)

            if (
                not fetched_data
                or (int(total_item) // filter.display) + 1 < filter.page
            ):
                break
            for item in fetched_data:
                total_law_data.append(item)
            filter.set_page(filter.page + 1)

        return total_law_data

    def fetch_law_list_data(self, filter: Filter) -> tuple[str, list[dict]]:
        """
        filter 조건에 맞춰서 http://www.law.go.kr/ 로부터 법령 목록을 fetch한다.
        """
        params = {}
        if filter.page is not None:
            params["page"] = filter.page
        if filter.query is not None:
            params["query"] = filter.query
        if filter.efYd is not None:
            params["efYd"] = filter.efYd
        if filter.org is not None:
            params["org"] = filter.org
        if filter.search is not None:
            params["search"] = filter.search
        if filter.display is not None:
            params["display"] = filter.display

        response = httpx.get(self.domain, params=params, timeout=30.0)
        response.raise_for_status()  # 요청 실패 시 예외 발생
        data = response.json()
        law_search = data.get("LawSearch", {})
        total_item = law_search.get("totalCnt", "0")
        if not law_search or "law" not in law_search:
            return total_item, []

        return total_item, law_search["law"]

    def _bulk_load_law_list_data(self, law_list_data: list):
        """
        법령 목록 데이터를 DB에 bulk load 한다.
        """
        bulk_objects = []

        for item in law_list_data:
            bulk_objects.append(
                KoLawList(
                    id=str(uuid.uuid4()),
                    현행연혁코드=item.get("현행연혁코드"),
                    법령일련번호=item.get("법령일련번호"),
                    자법타법여부=item.get("자법타법여부", ""),
                    법령상세링크=self.default_domain + item.get("법령상세링크"),
                    법령명한글=item.get("법령명한글"),
                    법령구분명=item.get("법령구분명"),
                    소관부처명=item.get("소관부처명"),
                    공포번호=item.get("공포번호"),
                    제개정구분명=item.get("제개정구분명"),
                    소관부처코드=item.get("소관부처코드"),
                    법령ID=item.get("법령ID"),
                    공동부령정보=item.get("공동부령정보", ""),
                    시행일자=item.get("시행일자"),
                    공포일자=item.get("공포일자"),
                    법령약칭명=item.get("법령약칭명", ""),
                )
            )

        try:
            # DB에 한 번에 저장
            KoLawList.objects.bulk_create(
                bulk_objects, ignore_conflicts=True
            )  # 중복된 경우 무시
            print(f"DB에 {len(bulk_objects)}개의 데이터를 저장했습니다.")
        except Exception as e:
            # 예외 발생 시, 디버깅 정보를 출력
            print("[ERROR] bulk_create 실패:")
            print(f"Exception: {e}")
            print("저장 시도한 데이터:")
            for obj in bulk_objects:
                print(vars(obj))

    def bulk_request_total_law_list_data(self):
        """
        admin 용임.
        http://www.law.go.kr/ 로부터 모든 법령 목록을 요청한다.
        페이지 처리를 확인하고 fetch_law_list_data를 반복 호출하여 전체 데이터를 가져온다.
        초기 세팅에 모든 법령 목록 데이터를 가져오기위함
        """
        filter = self.Filter(page=1, display=100)  # 첫 페이지부터 시작
        with transaction.atomic():
            while True:
                print(f"{filter.page} 페이지 데이터를 요청합니다...")
                _, law_data = self.fetch_law_list_data(filter)

                if not law_data:  # 더 이상 데이터가 없으면 종료
                    print("모든 데이터를 가져왔습니다.")
                    break

                self._bulk_load_law_list_data(law_data)  # 데이터를 DB에 저장
                filter.page += 1  # 다음 페이지 요청
