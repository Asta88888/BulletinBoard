from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from ads.models import Ad, Review
from ads.pagination import StandardResultPagination
from ads.serializer import AdSerializer, ReviewSerializer
from users.permissions import IsOwner, IsAdmin


class AdViewSet(ModelViewSet):
    """
    ViewSet для управления объявлениями.
    Позволяет создавать, просматривать, обновлять и удалять объявления.
    """
    serializer_class = AdSerializer
    queryset = Ad.objects.all()
    pagination_class = StandardResultPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save()

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = (IsAuthenticated,)
        elif self.action == 'list':
            self.permission_classes = (AllowAny,)
        elif self.action == 'retrieve':
            self.permission_classes = (IsAuthenticated,)
        elif self.action in ['update', 'destroy']:
            self.permission_classes = (IsOwner | IsAdmin)
        return super().get_permissions()

class ReviewViewSet(ModelViewSet):
    """
    ViewSet для управления отзывами.
    Позволяет создавать, просматривать, обновлять и удалять отзывы.
    """
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save()

    def get_permissions(self):
        if self.action in ['create', 'list', 'retrieve']:
            self.permission_classes = (IsAuthenticated,)
        elif self.action in ['update', 'destroy']:
            self.permission_classes = (IsOwner | IsAdmin)
        return super().get_permissions()
