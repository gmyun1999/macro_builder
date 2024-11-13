from django.urls import path

from macro_sheet.interface.view.worksheet_view import (
    GETMyWorksheetListView,
    MYWorksheetView,
    WorksheetValidatorView,
)
from macro_sheet.interface.views import TestView

urlpatterns = [
    path(
        "worksheet/validate/",
        view=WorksheetValidatorView.as_view(),
        name="validate_worksheet",
    ),
    path("function/validate/", view=TestView.as_view(), name="test"),
    path("me/function/<str:function_id>/", view=TestView.as_view(), name="test"),
    path("me/function/", view=TestView.as_view(), name="test"),
    path("me/functions/", view=TestView.as_view(), name="test"),
    path(
        "me/worksheet/<str:worksheet_id>/",
        view=MYWorksheetView.as_view(),
        name="my_worksheet",
    ),
    path("me/worksheet/", view=MYWorksheetView.as_view(), name="create_worksheet"),
    path(
        "me/worksheets/",
        view=GETMyWorksheetListView.as_view(),
        name="bulk_fetch_my_worksheets",
    ),
    path("gui/", view=TestView.as_view(), name="test"),
]
