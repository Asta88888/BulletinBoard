from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения и редактирования пользователя.
    """

    class Meta:
        model = User
        exclude = ["password"]


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации нового пользователя.
    """

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password"]

    def create(self, validated_data):
        """
        Создание пользователя с хэшированным паролем
        """
        user = User.objects.create(email=validated_data["email"], is_active=True)
        user.set_password(validated_data["password"])
        user.save()
        return user
