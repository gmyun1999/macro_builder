from django.conf.urls.static import static
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from macro_be import settings
from macro_be.views import HealthChecker
from macro_sheet.interface import urls as macro_urls
from user.interface import urls as user_urls

schema_view = get_schema_view(
    openapi.Info(
        title="macro-be API",
        default_version="v1",
        description="API documentation for the macro-be project",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path(r"^$", view=HealthChecker.as_view(), name="HealthChecker"),
    re_path(r"^", include(user_urls)),
    re_path(r"^", include(macro_urls)),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
