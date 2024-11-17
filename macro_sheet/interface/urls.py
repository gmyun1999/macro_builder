from django.urls import path

from macro_sheet.interface.view.function_view import (
    FunctionValidatorView,
    GETMyFunctionListView,
    MYBlockFunctionView,
)
from macro_sheet.interface.view.gui_view import GenerateGuiView
from macro_sheet.interface.view.worksheet_view import (
    GETMyWorksheetListView,
    MYWorksheetView,
    WorksheetValidatorView,
)

urlpatterns = [
    path(
        "worksheet/validate/",
        view=WorksheetValidatorView.as_view(),
        name="validate_worksheet",
    ),
    path(
        "function/validate/",
        view=FunctionValidatorView.as_view(),
        name="function_validate",
    ),
    path(
        "me/function/<str:function_id>/",
        view=MYBlockFunctionView.as_view(),
        name="my_function",
    ),
    path("me/function/", view=MYBlockFunctionView.as_view(), name="my_function"),
    path(
        "me/functions/",
        view=GETMyFunctionListView.as_view(),
        name="bulk_fetch_my_functions",
    ),
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
    path("gui/", view=GenerateGuiView.as_view(), name="generate_gui"),
]
