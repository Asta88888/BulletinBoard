from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    """
    Команда для создания суперпользователя с ролью 'admin'.
    """
    def handle(self, *args, **kwargs):
        User = get_user_model()
        user, created = User.objects.get_or_create(
            email="admin@example.com",
            defaults={
                "role": User.ADMIN,
            }
        )
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        if created:
            user.set_password("101208")
        user.save()
        self.stdout.write(self.style.SUCCESS(f"Суперпользователь {user.email} готов."))
