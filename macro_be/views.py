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


def swagger_html_view(request):
    schema_generator = OpenAPISchemaGenerator(
        info=openapi.Info(
            title="Your API",  # API 제목
            default_version="1.0.0",  # 버전을 명확히 설정
            description="API 문서",  # 설명
            terms_of_service="https://www.google.com/policies/terms/",
            contact=openapi.Contact(email="contact@example.com"),
            license=openapi.License(name="BSD License"),
        )
    )

    # 스키마 생성 시 request=None으로 설정하여 호환성 유지
    schema = schema_generator.get_schema(request=None, public=True)
    renderer = SwaggerUIRenderer()
    renderer_context = {
        "request": request,
        "url": request.build_absolute_uri(),
    }

    # HTML 콘텐츠 생성 및 반환
    html_content = renderer.render(schema, renderer_context=renderer_context)
    return HttpResponse(html_content, content_type="text/html")
