from django.contrib.auth import get_user_model
from django.core.management import BaseCommand


class Command(BaseCommand):
    """
    Команда для создания суперпользователя с ролью 'admin'.
    """

    def handle(self, *args, **kwargs):
        """
        Создаёт суперпользователя, если он отсутствует,
        или обновляет права существующего пользователя.
        """
        User = get_user_model()
        user, created = User.objects.get_or_create(
            email="admin@example.com",
            defaults={
                "role": User.ADMIN,
            },
        )
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        if created:
            user.set_password("101208")
        user.save()
        self.stdout.write(self.style.SUCCESS(f"Суперпользователь {user.email} готов."))
