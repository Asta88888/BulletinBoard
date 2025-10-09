from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Модель пользователя. В качестве логина используется email.
    """

    username = None
    USER = "user"
    ADMIN = "admin"
    ROLE_CHOICES = [
        (USER, "Пользователь"),
        (ADMIN, "Администратор"),
    ]
    first_name = models.CharField(max_length=50, verbose_name="Имя", help_text="Введите имя", blank=True, null=True)
    last_name = models.CharField(
        max_length=50, verbose_name="Фамилия", help_text="Введите фамилию", blank=True, null=True
    )
    phone = models.CharField(
        max_length=35, verbose_name="Телефон", blank=True, null=True, help_text="Введите номер телефона"
    )
    email = models.EmailField(unique=True, verbose_name="Почта", help_text="Введите почту")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=USER, verbose_name="Роль")
    image = models.ImageField(
        upload_to="users/avatars/", blank=True, null=True, verbose_name="Аватар", help_text="Загрузите аватар"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        """
        Строковое представление модели пользователя.
        """
        return f"{self.email} ({self.get_role_display()})"
