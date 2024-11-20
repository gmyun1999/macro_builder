from django.urls import include, path, re_path
from drf_spectacular.views import SpectacularAPIView

from macro_be.views import HealthChecker
from macro_sheet.interface import urls as macro_urls
from user.interface import urls as user_urls

urlpatterns = [
    re_path(r"^$", view=HealthChecker.as_view(), name="HealthChecker"),
    re_path(r"^", include(user_urls)),
    re_path(r"^", include(macro_urls)),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
]
