from django.db import models
from users.models import User


class Ad(models.Model):
    """
    Модель объявления.
    """
    title = models.CharField(max_length=150, verbose_name='Название', help_text='Введите название товара')
    price = models.PositiveIntegerField(verbose_name='Цена', help_text='Введите цену товара')
    description = models.TextField(verbose_name='Описание товара', help_text='Введите описание товара')
    author = models.ForeignKey(User, verbose_name='Создатель объявления', related_name='ads', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ['-created_at']

    def __str__(self):
        """
        Строковое представление модели объявления.
        """
        return f"{self.title} - {self.price}₽"

class Review(models.Model):
    """
    Модель отзыва.
    """
    text = models.TextField(verbose_name='Отзыв', help_text='Напишите отзыв')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор отзыва', related_name='reviews')
    ad = models.ForeignKey(Ad, related_name='reviews', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at']

    def __str__(self):
        """
        Строковое представление модели отзыва.
        """
        return f"Отзыв от {self.author} к объявлению {self.ad}"
