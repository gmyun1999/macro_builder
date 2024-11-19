from django.http import HttpResponse, JsonResponse
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.renderers import SwaggerUIRenderer
from rest_framework import status
from rest_framework.views import APIView

from macro_be.settings import ENV


class HealthChecker(APIView):
    def get(self, request):
        return JsonResponse(
            data={"status": "success", "ENV": ENV},
            status=status.HTTP_200_OK,
        )
