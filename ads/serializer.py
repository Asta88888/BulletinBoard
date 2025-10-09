from rest_framework.serializers import ModelSerializer
from ads.models import Ad, Review


class AdSerializer(ModelSerializer):
    """
    Сериализатор для модели `Ad`.
    Используется для преобразования объектов объявлений в JSON и обратно.
    Поле `author` доступно только для чтения и автоматически заполняется
    текущим пользователем при создании объявления.
    """

    class Meta:
        model = Ad
        fields = "__all__"
        read_only_fields = ("author",)


class ReviewSerializer(ModelSerializer):
    """
    Сериализатор для модели `Review`.

    Преобразует объекты отзывов в JSON и обратно.
    Поле `author` доступно только для чтения и автоматически заполняется
    текущим пользователем при создании отзыва.
    """

    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ("author",)
