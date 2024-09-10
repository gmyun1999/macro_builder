from django.urls import path

from user.interface.views.user_views import OAuthLoginView, RefreshTokenView

urlpatterns = [
    path("user/token-refresh", view=RefreshTokenView.as_view(), name="tokenRefresh"),
    path(
        "user/login/<str:auth_server>", view=OAuthLoginView.as_view(), name="oauthLogin"
    ),
]
