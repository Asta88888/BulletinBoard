from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

from ads.apps import AdsConfig
from ads.views import AdViewSet, ReviewViewSet

app_name = AdsConfig.name

router = SimpleRouter()
router.register("", AdViewSet, basename="ad")

reviews_router = routers.NestedSimpleRouter(router, "", lookup="ad")
reviews_router.register("reviews", ReviewViewSet, basename="ad-reviews")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(reviews_router.urls)),
]
