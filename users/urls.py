from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from users.views import UserCreateAPIView, UserListAPIView, UserRetrieveAPIView, UserUpdateAPIView, UserDestroyAPIView
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from django.urls import path
from users.apps import UsersConfig
from rest_framework.permissions import AllowAny


app_name = UsersConfig.name

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
    path('list/', UserListAPIView.as_view(), name='users_list'),
    path('detail/<int:pk>/', UserRetrieveAPIView.as_view(), name='user_detail'),
    path('update/<int:pk>/', UserUpdateAPIView.as_view(), name='user_update'),
    path('destroy/<int:pk>/', UserDestroyAPIView.as_view(), name='user_destroy'),
    # path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    # path('password-reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('password-reset/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
