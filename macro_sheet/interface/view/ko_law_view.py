import csv
import gzip
import io
from dataclasses import dataclass

from django.http import HttpResponse
from pydantic import BaseModel, Field
from rest_framework.views import APIView

from common.interface.response import error_response, success_response
from common.interface.validators import validate_body
from macro_be import settings
from macro_sheet.infra.ko_law_api_server import KoLawApiServer
from macro_sheet.service.service.ko_law_service import KoLawService


class FetchKoLawApi(APIView):
    """
    한국법령 조회 API
    """

    @dataclass
    class BodyData(BaseModel):
        access_key: str = Field()  # 접근키
        query: str = Field(default=None)  # 검색어
        efYd: str = Field(
            default=None, min_length=17, max_length=17
        )  # 시행일자 범위 예: "20090101~20090130"
        org_name: str = Field(default=None, min_length=1, max_length=30)  # 소관부처 이름

    def __init__(self):
        self.ko_law_servicer = KoLawApiServer(oc=settings.KO_LAW_OC)
        self.ko_law_service = KoLawService()

    @validate_body(BodyData)
    def post(self, request, body: BodyData):
        if body.access_key != settings.COMMAND_GUI_ACCESS_KEY:
            return error_response(
                code="ACCESS_DENIED", message="접근 권한이 없습니다.", status=403
            )

        if body.org_name is not None:
            org = self.ko_law_service.get_org(org_name=body.org_name)

        filter = self.ko_law_servicer.Filter(query=body.query, efYd=body.efYd, org=org)
        list_law_data = self.ko_law_servicer.auth_fetch_law_list_data(filter=filter)

        output = io.BytesIO()
        with gzip.GzipFile(fileobj=output, mode="wb") as gz:
            if list_law_data:  # 데이터가 있는 경우
                writer = csv.DictWriter(
                    io.TextIOWrapper(gz, encoding="utf-8-sig"),
                    fieldnames=list_law_data[0].keys(),
                )
                writer.writeheader()
                writer.writerows(list_law_data)
            else:  # 데이터가 없는 경우
                # 빈 헤더만 작성
                writer = csv.DictWriter(
                    io.TextIOWrapper(gz, encoding="utf-8-sig"), fieldnames=["No Data"]
                )
                writer.writeheader()

        # 스트림 포인터를 시작으로 이동
        output.seek(0)

        # HTTP 응답 생성
        response = HttpResponse(output, content_type="application/gzip")
        response["Content-Disposition"] = 'attachment; filename="law_data.csv.gz"'
        return response
