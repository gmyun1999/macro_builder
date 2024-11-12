from dataclasses import dataclass

from django.http import JsonResponse
from pydantic import BaseModel, Field
from rest_framework import status
from rest_framework.views import APIView

from common.interface.validators import validate_body
from macro_sheet.domain.block_serializer import GenericSerializer


class TestView(APIView):
    """
    우선 block 하나를 받았을때 잘 반환하는지를 테스트 하겠음.
    """

    @dataclass
    class BodyParams(BaseModel):
        data: int = Field(gt=0)

    @validate_body(BodyParams)
    def post(self, request, body):
        pass
