from typing import Any

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.auth_system.apis.AuthJWTAPI import AuthJWTAPI, check

app_name: str = 'auth_system'
urlpatterns: list[Any] = [

    path('login/', AuthJWTAPI.as_view({'post': 'login'}), name='AuthJWTSystemLogin'),
    path('register/', AuthJWTAPI.as_view({'post': 'register'}), name='AuthJWTSystemRegister'),
    path('refresh/', TokenRefreshView.as_view(), name='AuthJWTSystemTokenRefresh'),
    path('check/', check, name='AuthJWTSystemCheckUser'),

    path('reset_password/', AuthJWTAPI.as_view(({"post": "reset_password"})), name='AuthResetPassword'),
    path('get_permission/', AuthJWTAPI.as_view({'post': 'get_permission'}), name='AuthJWTSystemGetPermission'),
]
