from dataclasses import dataclass

from pydantic import BaseModel, Field
from rest_framework.views import APIView

from common.interface.validators import validate_body
from macro_sheet.domain.block_serializer import GenericSerializer


class TestView(APIView):
    """
    우선 block 하나를 받았을때 잘 반환하는지를 테스트 하겠음.
    """

    @dataclass
    class BodyParams(BaseModel):
        data: dict = Field()

    @validate_body(BodyParams)
    def post(self, request, body):
        block_dict = body.data
        # 얘를 도메인 객체로 매핑해줘야함.
        # dict 을 저장한다
        serializer = GenericSerializer(block_dict)
        if serializer.is_valid():
            domain = serializer.to_domain_object()
        # 도메인 객체를 저장한다.
        # 도메인 객체를 jinja2 템플릿으로 변경시킨다.
        # 생성한 템플릿을 json으로 패키지 서버로 보낸다.
