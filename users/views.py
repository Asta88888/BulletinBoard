from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import status
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from config.settings import EMAIL_HOST_USER
from users.models import User
from users.permissions import IsAdmin, IsAdminOrSelf
from users.serializer import UserCreateSerializer, UserSerializer


class UserCreateAPIView(CreateAPIView):
    """
    Эндпоинт для регистрации нового пользователя.
    """

    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)


class UserListAPIView(ListAPIView):
    """
    Эндпоинт для получения списка всех пользователей (только для администраторов).
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdmin]


class UserRetrieveAPIView(RetrieveAPIView):
    """
    Эндпоинт для получения информации о конкретном пользователе.
    Доступен либо администратору, либо самому пользователю.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminOrSelf]


class UserUpdateAPIView(UpdateAPIView):
    """
    Эндпоинт для обновления информации о пользователе.
    Доступен администратору или владельцу профиля.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminOrSelf]


class UserDestroyAPIView(DestroyAPIView):
    """
    Эндпоинт для удаления пользователя.
    Доступен администратору или самому пользователю.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminOrSelf]


class PasswordResetView(APIView):
    """
    Эндпоинт для инициализации процесса сброса пароля.
    Отправляет на email пользователя ссылку для восстановления пароля.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Отправляет письмо со ссылкой для сброса пароля.
        """
        email = request.data.get("email")
        user = User.objects.get(email=email)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        frontend_url = "http://127.0.0.1:8000"
        reset_link = f"{frontend_url}/users/password-reset/{uid}/{token}/"

        send_mail(
            subject="Password Reset",
            message=f"Click the link to reset your password: {reset_link}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return Response({"detail": "Password reset email sent."}, status=status.HTTP_200_OK)


class PasswordResetDoneView(APIView):
    """
    Эндпоинт для отображения уведомления после отправки ссылки на сброс пароля.
    """

    permission_classes = [AllowAny]

    def get(self, request):
        """
        Возвращает уведомление о необходимости проверить почту.
        """
        return Response({"detail": "Please check your email for the password reset link."})


class PasswordResetConfirmView(APIView):
    """
    Эндпоинт для подтверждения и установки нового пароля.
    """

    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        """
        Устанавливает новый пароль для пользователя.
        """
        password = request.data.get("password")
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        user.set_password(password)
        user.save()
        return Response({"detail": "Password has been reset successfully."}, status=status.HTTP_200_OK)


class PasswordResetCompleteView(APIView):
    """
    Эндпоинт для отображения уведомления после успешного сброса пароля.
    """

    permission_classes = [AllowAny]

    def get(self, request):
        """
        Возвращает сообщение о том, что пароль успешно изменён.
        """
        return Response({"detail": "Your password has been reset. You can now log in with the new password."})
