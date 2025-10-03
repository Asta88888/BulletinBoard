from rest_framework.serializers import ModelSerializer
from ads.models import Ad, Review


class AdSerializer(ModelSerializer):
    class Meta:
        model = Ad
        fields = "__all__"

class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"
