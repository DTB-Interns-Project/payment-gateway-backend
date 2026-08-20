from django.urls import include, path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import MeView, RegisterView, ProfileView


urlpatterns = [
    path(
        "auth/register/",
        RegisterView.as_view(),
        name="register",
    ),

    path(
        "auth/login/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),

    path(
        "auth/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),

    path(
        "auth/me/",
        MeView.as_view(),
        name="me",
    ),

    path(
        "wallet/",
        include("wallets.urls"),
    ),
    path(
        "profile/", 
        ProfileView.as_view(), 
        name="profile"
        ),
]