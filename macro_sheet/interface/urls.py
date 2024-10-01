from django.urls import path

from macro_sheet.interface.views import TestView

urlpatterns = [
    path("test/", view=TestView.as_view(), name="test"),
]
