from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from .views import UserLoginView, UserRegisterView

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path(
        "refresh/",
        TokenRefreshView.as_view(),
        name="refresh_token",
    ),
    path(
        "verify/",
        TokenVerifyView.as_view(),
        name="verify_token",
    ),
]
